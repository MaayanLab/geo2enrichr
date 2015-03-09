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


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    session = Session()
    try:
        yield session
        # The ORM is responsible for committing the session.
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
        session.commit()
        return instance


def save_softfile(softfile):
    """Single entry point for saving classes to database.
    """
    with session_scope() as session:
        softfile_db = models.SoftFile(name=softfile.name, is_geo=softfile.is_geo)
        session.add(softfile_db)
        session.commit()
        return softfile_db.id


def save_genelist(genelist):
    with session_scope() as session:
        import pdb; pdb.set_trace()
        ranked_genes_up = []
        for gene_name,rank in genelist.up:
            gene_db = get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_db = get_or_create(session, models.RankedGene, gene_id=gene_db.id, rank=rank)
            ranked_genes_up.append(ranked_gene_db)

        import pdb; pdb.set_trace()
        ranked_genes_down = []
        for gene_name,rank in genelist.down:
            gene_db = get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_db = get_or_create(session, models.RankedGene, gene_id=gene_db.id, rank=rank)
            ranked_genes_down.append(ranked_gene_db)

        import pdb; pdb.set_trace()
        genelist_db = models.GeneList(
            up = ranked_genes_up,
            down = ranked_genes_down,
            diff_exp_method = genelist.method,
            cutoff = genelist.cutoff,
            enrichr_link_up = genelist.enrichr_link_up,
            enrichr_link_down = genelist.enrichr_link_down
        )
        session.add(genelist_db)
        session.commit()
        return genelist_db.id


def fetch(obj):
    """Single entry point for fetching data from database.
    """
    pass


def build_probe_dict(platform_probesetid_genesym_file):
    """Builds an in-memory dictionary mapping platforms to probe IDs to gene
    symbols.
    """
    # Platform data collected and script written by Andrew Rouillard.
    platform_dict = {}
    with open(platform_probesetid_genesym_file) as f:
        for line in f:
            entries = line.rstrip().split('\t')
            platform = entries[0]
            probesetid = entries[1]
            genesym = entries[2]
            if platform in platform_dict:
                platform_dict[platform][probesetid] = genesym
            else:
                platform_dict[platform] = {probesetid:genesym}
    return platform_dict


PROBE2GENE = build_probe_dict('orm/probe2gene.txt')




'''
def save_soft_file(soft_file):
    with session_scope() as session:
        soft_file_db = models.SoftFile(name=soft_file.name, is_geo=soft_file.is_geo)
        session.add(soft_file_db)
        session.commit()
        db_id = soft_file_db.id
        soft_file.db_id = db_id
        return db_id


def fetch_soft_file(soft_file):
    with session_scope() as session:
        query = session.query(models.SoftFile).filter_by(id=soft_file.db_id)
        return query.first()
'''
