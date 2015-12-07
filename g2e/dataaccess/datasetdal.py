"""Handles all database transactions for the Dataset class.
"""


import sqlalchemy as sa

from g2e.dataaccess.util import session_scope
from g2e.model.geodataset import GeoDataset


def get(accession):
    with session_scope() as session:
        instance = session.query(GeoDataset)\
            .filter_by(accession=accession)\
            .first()
        return instance
