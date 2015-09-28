"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dataaccess.util import session_scope
from g2e.model.genesignature import GeneSignature
from g2e.model.tag import Tag
from g2e.model.optionalmetadata import OptionalMetadata


def fetch_all(klass):
    """Fetches all entities of a specific class.
    """
    with session_scope() as session:
        return session.query(klass).all()


def save_gene_signature(gene_signature):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        session.add(gene_signature)
        session.commit()
        return gene_signature.extraction_id


def fetch_gene_signature(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .first()


def fetch_tag(tag_name):
    """Fetches tags based on name.
    """
    with session_scope() as session:
        return session\
            .query(Tag)\
            .filter(Tag.name == tag_name)\
            .first()


def fetch_metadata(metadata_name):
    """Fetches metadata based on name.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .all()


def fetch_metadata_by_value(metadata_name, metadata_value):
    """Fetches metadata based on name and value.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .filter(OptionalMetadata.value == metadata_value)\
            .all()