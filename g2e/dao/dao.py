"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

from contextlib import contextmanager

from g2e.app import db
import g2e.orm.models as models
from g2e.core.genelist.genelist import GeneList
from g2e.core.metadata.metadata import Metadata
from g2e.core.extraction.extraction import Extraction


def save(extraction):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    softfile_dao = extraction.softfile
    gls = extraction.genelists
    metadata = extraction.metadata

    print 'saving extraction'

    with session_scope() as session:

        print 'softfile DAO created'

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
                    name           = gl.name,
                    ranked_genes   = ranked_genes,
                    direction      = gl.direction,
                    text_file      = gl.text_file,
                    enrichr_link   = gl.target_apps['enrichr'],
                    l1000cds2_link = gl.target_apps['l1000cds2'],
                    paea_link      = gl.target_apps['paea']
                )
            )

            print 'gene list DAO created'

        print 'all gene list DAOs created'

        extraction_dao = models.Extraction(
            extraction_id     = extraction.extraction_id,
            softfile          = softfile_dao,
            genelists         = genelists_dao,
            cutoff            = metadata.cutoff,
            threshold         = metadata.threshold,
            organism          = metadata.organism,
            cell              = metadata.cell,
            perturbation      = metadata.perturbation,
            gene              = metadata.gene,
            disease           = metadata.disease
        )

        diff_exp_method_dao = models.DiffExpMethod(
            name = metadata.diffexp_method,
            extraction = extraction_dao
        )
        ttest_correction_method_dao = models.TtestCorrectionMethod(
            name = metadata.correction_method,
            extraction = extraction_dao
        )

        session.add_all([
            softfile_dao,
            diff_exp_method_dao,
            ttest_correction_method_dao,
            extraction_dao
        ])

        session.commit()
        return extraction_dao.extraction_id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:

        ext_dao = session.query(models.Extraction).filter_by(extraction_id=extraction_id).first()

        softfile  = ext_dao.softfile

        #name      = sf_dao.name
        #text_file = sf_dao.text_file
        #is_geo    = sf_dao.is_geo
        #normalize = sf_dao.normalize
        #platform  = sf_dao.platform
        #softfile  = SoftFile.from_db(name, platform, text_file, is_geo, normalize)

        metadata   = Metadata(
            ext_dao.diff_exp_method.name,
            ext_dao.cutoff,
            ext_dao.ttest_correction_method.name,
            ext_dao.threshold,
            ext_dao.organism,
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
            target_apps = {
                'enrichr'  : gl_dao.enrichr_link,
                'l1000cds2': gl_dao.l1000cds2_link,
                'paea'     : gl_dao.paea_link
            }
            genelists.append(
                GeneList(
                    ranked_genes,
                    direction,
                    metadata,
                    target_apps,
                    name=name,
                    text_file=text_file
                )
            )

        session.commit()
        return Extraction(softfile, genelists, metadata)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    try:
        yield db.session
        db.session.commit()
    except Exception as e:
        print 'Rolling back database'
        print e
        db.session.rollback()


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