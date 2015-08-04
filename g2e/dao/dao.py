"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

from contextlib import contextmanager

from g2e.app import db
from g2e.model.extraction import Extraction


def save(extraction):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        session.add(extraction)
        session.commit()
        return extraction.extraction_id


def fetch(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        extraction = session.query(Extraction).filter_by(extraction_id=extraction_id).first()
        return extraction


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    try:
        yield db.session
        db.session.commit()
    except Exception as e:
        print 'Rolling back database'
        print e
        db.session.rollback()