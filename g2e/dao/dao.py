"""This module handles all database transactions. It has knowledge of the two
primary class, GeneList and SoftFile, and saves them accordingly.
"""


import copy
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from orm.commondb import Base, engine
import orm.models as models


Session = sessionmaker()
Session.configure(bind=engine)

# Does this need to run every time?
Base.metadata.create_all(engine)


def save(extraction):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    sf = extraction.softfile
    gl = extraction.genelist
    
    with session_scope() as session:

        softfile_dao  = models.SoftFile(
            name      = sf.name,
            platform  = sf.platform,
            is_geo    = sf.is_geo,
            text_file = sf.text_file
        )

        ranked_genes = []
        for gene_name,rank in gl.ranked_genes:
            gene_dao = _get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_dao = models.RankedGene(
                gene = gene_dao,
                rank = rank
            )
            ranked_genes.append(ranked_gene_dao)

        genelist_dao = models.GeneList(
            ranked_genes = ranked_genes,
            text_file = gl.text_file
        )
        
        extraction_dao = models.Extraction(
            softfile          = softfile_dao,
            genelist          = genelist_dao,
            method            = extraction.method,
            cutoff            = extraction.cutoff,
            enrichr_link_up   = extraction.enrichr_link_up,
            enrichr_link_down = extraction.enrichr_link_down,
        )

        session.add(extraction_dao)
        session.flush()
        return extraction_dao.id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        ext_dao = session.query(models.Extraction).filter_by(id=extraction_id).first()
        results = copy.deepcopy(ext_dao.__dict__)
        softfile = copy.deepcopy(ext_dao.softfile.__dict__)
        genelist = copy.deepcopy(ext_dao.genelist.__dict__)
        ranked_genes = ext_dao.genelist.ranked_genes

        results['softfile'] = softfile
        results['genelist'] = genelist
        results['genelist']['ranked_genes'] = [(rg.gene.name,rg.rank) for rg in ranked_genes]
        return results


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


def _clean_sqlalchemy_dict(obj):
    del obj['_sa_instance_state']
    del obj['genelist_id']
    del obj['softfile_id']
    del obj['softfile']['_sa_instance_state']
    del obj['genelist']['_sa_instance_state']
    return obj
