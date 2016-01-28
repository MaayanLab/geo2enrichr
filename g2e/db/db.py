"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.
"""

from substrate import GeneSignature
from substrate import GeoDataset

from g2e.db.utils import session_scope


def save_gene_signature(gene_signature):
    """Saves a gene signature and returns the extraction ID.
    """
    with session_scope() as session:
        session.add(gene_signature)
        session.commit()
        return gene_signature.extraction_id


def get_gene_signature(extraction_id):
    """Returns gene signature based on extraction ID.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .first()


def get_geo_dataset(accession):
    """Returns a GEO dataset based on accession number.
    """
    with session_scope() as session:
        instance = session.query(GeoDataset)\
            .filter_by(accession=accession)\
            .first()
        return instance


def get_num_gene_signatures():
    """Returns the number of gene signatures in the database.
    """
    with session_scope() as session:
        return session.query(GeneSignature).count()
