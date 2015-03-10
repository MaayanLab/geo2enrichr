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


def save_softfile(softfile):
    with session_scope() as session:
        softfile_db = models.SoftFile(name=softfile.name, is_geo=softfile.is_geo)
        session.add(softfile_db)
        session.commit()
        return softfile_db.id


def save_genelist(genelist):
    with session_scope() as session:
        ranked_genes = []
        for gene_name,rank in genelist.ranked_genes:
            gene_db = get_or_create(session, models.Gene, name=gene_name)
            ranked_gene_db = models.RankedGene(gene_id=gene_db.id, rank=rank)
            ranked_genes.append(ranked_gene_db)

        genelist_db = models.GeneList(
            genes = ranked_genes,
            diff_exp_method = genelist.method,
            cutoff = genelist.cutoff,
            enrichr_link_up = genelist.enrichr_link_up,
            enrichr_link_down = genelist.enrichr_link_down
        )
        session.add(genelist_db)
        session.commit()
        return genelist_db.id


def save_extraction(softfile_id, genelist_id):
	with session_scope() as session:
		extraction_db = models.Extraction(
			softfile_id=softfile_id,
			genelist_id=genelist_id
		)
		session.add(extraction_db)
		session.commit()
		return extraction_db.id


def fetch_extraction(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    result = {}
    with session_scope() as session:
    	extraction = session.query(models.Extraction).filter_by(id=extraction_id).first()
    	softfile = session.query(models.SoftFile).filter_by(id=extraction.softfile_id).first()
    	result['dataset'] = softfile.name
    	#result['platform'] = softfile.platform
    	return result


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
        session.flush()
        return instance


PROBE2GENE = build_probe_dict('orm/probe2gene.txt')
