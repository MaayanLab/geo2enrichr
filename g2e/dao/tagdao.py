"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dao.util import session_scope
from g2e.model.metadatatag import MetadataTag


def fetch(tag_name):
    """Single entry point for fetching extractions from database by ID.
    """
    print 'Fetching metadata tag ' + tag_name
    with session_scope() as session:
        tag = session.query(MetadataTag).filter_by(name=tag_name).first()
        return tag