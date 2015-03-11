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

        softfile_dao = models.SoftFile(
            name     = sf.name,
            platform = sf.platform,
            is_geo   = sf.is_geo,
            genes    = sf.genes
        )

        ranked_genes = []
        for gene_name,rank in gl.ranked_genes:
            gene_dao = get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_dao = models.RankedGene(
                gene = gene_dao,
                rank = rank
            )
            ranked_genes.append(ranked_gene_dao)

        genelist_dao = models.GeneList(
            ranked_genes = ranked_genes,
        )
        import pdb; pdb.set_trace()
        
        extraction_dao = models.Extraction(
            softfile          = softfile_dao,
            genelist          = genelist_dao,
            method            = extraction.method,
            cutoff            = extraction.cutoff,
            enrichr_link_up   = extraction.enrichr_link_up,
            enrichr_link_down = extraction.enrichr_link_down
        )

        session.add(extraction_dao)
        session.flush()
        return extraction_dao.id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        extraction_dao = session.query(models.Extraction).filter_by(id=extraction_id).first()
        softfile_dao = extraction_dao.softfile
        genelist_dao = extraction_dao.genelist

        result = copy.deepcopy(extraction_dao.__dict__)
        result['softfile'] = softfile_dao.name
        result['platform'] = softfile_dao.platform
        result['genelist'] = [(rg.gene.name,rg.rank) for rg in genelist_dao.ranked_genes]
        return clean_sqlalchemy_dict(result)


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


def get_or_create(session, model, **kwargs):
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


def clean_sqlalchemy_dict(obj):
    del obj['_sa_instance_state']
    del obj['genelist_id']
    del obj['softfile_id']
    del obj['id']
    return obj
