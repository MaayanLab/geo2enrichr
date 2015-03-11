"""This module handles all database transactions. It has knowledge of the two
primary class, GeneList and SoftFile, and saves them accordingly.
"""


from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from orm.commondb import Base, engine
import orm.models as models


Session = sessionmaker()
Session.configure(bind=engine)

# Does this need to run every time?
Base.metadata.create_all(engine)


def save(softfile, genelist):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        softfile_dao = models.SoftFile(name=softfile.name, is_geo=softfile.is_geo)
        session.add(softfile_dao)

        ranked_genes = []
        for gene_name,rank in genelist.ranked_genes:
            gene_dao = get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_dao = models.RankedGene(gene_id=gene_dao.id, rank=rank)
            ranked_genes.append(ranked_gene_dao)

        genelist_dao = models.GeneList(
            genes = ranked_genes,
            diff_exp_method = genelist.method,
            cutoff = genelist.cutoff,
            enrichr_link_up = genelist.enrichr_link_up,
            enrichr_link_down = genelist.enrichr_link_down
        )

        extraction_dao = models.Extraction(
            softfile_id=softfile_dao.id,
            genelist_id=genelist_dao.id
        )
        session.add(extraction_dao)
        
        session.flush()
        return extraction_dao.id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    result = {}
    with session_scope() as session:
        extraction_dao = session.query(models.Extraction).filter_by(id=extraction_id).first()
        softfile = session.query(models.SoftFile).filter_by(id=extraction_dao.softfile_id).first()
        result['dataset'] = softfile.name
        return result


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
