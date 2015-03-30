"""This module handles all database transactions. It has knowledge of the two
primary class, GeneList and SoftFile, and saves them accordingly.
"""


import copy
from contextlib import contextmanager

from g2e.orm.commondb import Session
import g2e.orm.models as models
from g2e.core.genelist.genelist import GeneList
from g2e.core.softfile.softfile import SoftFile
from g2e.core.metadata.metadata import Metadata
from g2e.core.extraction.extraction import Extraction


def save(extraction):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    sf = extraction.softfile
    gls = extraction.genelists
    metadata = extraction.metadata

    with session_scope() as session:
        softfile_dao  = models.SoftFile(
            name      = sf.name,
            platform  = sf.platform,
            is_geo    = sf.is_geo,
            text_file = sf.text_file
        )

        genelists_dao = []
        for gl in gls:
            ranked_genes = []
            for gene_name,value in gl.ranked_genes:
                gene_dao = _get_or_create(session, models.Gene, name=gene_name)
                ranked_gene_dao = models.RankedGene(
                    gene  = gene_dao,
                    value = value
                )
                ranked_genes.append(ranked_gene_dao)

            genelists_dao.append(
                models.GeneList(
                    name = gl.name,
                    ranked_genes = ranked_genes,
                    direction = gl.direction,
                    text_file = gl.text_file,
                    enrichr_link = gl.enrichr_link
                )
            )

        extraction_dao = models.Extraction(
            extraction_id = extraction.extraction_id,
            softfile      = softfile_dao,
            genelists     = genelists_dao,
            method        = metadata.method,
            cutoff        = metadata.cutoff,
            cell          = metadata.cell,
            perturbation  = metadata.perturbation,
            gene          = metadata.gene,
            disease       = metadata.disease
        )

        session.add(extraction_dao)
        session.flush()
        return extraction_dao.extraction_id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        ext_dao = session.query(models.Extraction).filter_by(extraction_id=extraction_id).first()

        sf_dao    = ext_dao.softfile
        name      = sf_dao.name
        text_file = sf_dao.text_file
        is_geo    = sf_dao.is_geo
        platform  = sf_dao.platform
        softfile  = SoftFile(name, platform=platform, text_file=text_file, is_geo=is_geo)
        metadata  = Metadata(
            ext_dao.method,
            ext_dao.cutoff,
            ext_dao.cell,
            ext_dao.perturbation,
            ext_dao.gene,
            ext_dao.disease
        )

        genelists = []
        for gl_dao in ext_dao.genelists:
            name = gl_dao.name
            ranked_genes = [(r.gene.name,r.value) for r in gl_dao.ranked_genes]
            direction = gl_dao.direction
            text_file = gl_dao.text_file
            enrichr_link = gl_dao.enrichr_link
            genelists.append(
                GeneList(
                    ranked_genes,
                    direction,
                    metadata,
                    name=name,
                    text_file=text_file,
                    enrichr_link=enrichr_link
                )
            )

        return Extraction(softfile, genelists, metadata)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def _get_or_create(session, model, **kwargs):
    """Returns an instance of the database object, creating one if necessary.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance
