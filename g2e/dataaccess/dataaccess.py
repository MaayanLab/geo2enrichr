"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dataaccess.util import session_scope
from g2e.model.extraction import Extraction
from g2e.model.metadatatag import MetadataTag


def save_extraction(extraction):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        session.add(extraction)
        session.commit()
        return extraction.extraction_id


def fetch_extraction(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    print 'Fetching extraction_id ' + extraction_id
    with session_scope() as session:
        extraction = session.query(Extraction).filter_by(extraction_id=extraction_id).first()
        return extraction


def fetch_metadata_tag(tag_name):
    """Single entry point for fetching extractions from database by ID.
    """
    print 'Fetching metadata tag ' + tag_name
    with session_scope() as session:
        tag = session.query(MetadataTag).filter_by(name=tag_name).first()
        return tag