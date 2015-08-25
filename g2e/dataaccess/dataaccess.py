"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dataaccess.util import session_scope
from g2e.model.genesignature import GeneSignature
from g2e.model.metadatatag import MetadataTag
from g2e.model.optionalmetadata import OptionalMetadata


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
    print 'Fetching extraction_id ' + extraction_id
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(extraction_id == extraction_id)\
            .first()


def fetch_tag(tag_name):
    """Fetches tags based on name.
    """
    print 'Fetching tag ' + tag_name
    with session_scope() as session:
        return session\
            .query(MetadataTag)\
            .filter(tag_name == tag_name)\
            .first()


def fetch_metadata(metadata_name):
    """Fetches metadata based on name.
    """
    print 'Fetching metadata ' + metadata_name
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(metadata_name == metadata_name)\
            .first()


def fetch_metadata_by_value(metadata_name, metadata_value):
    """Fetches metadata based on name and value.
    """
    print 'Fetching metadata ' + metadata_name
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .filter(OptionalMetadata.value == metadata_value)\
            .all()