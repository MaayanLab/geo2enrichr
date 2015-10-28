"""Handles all database transactions for the Dataset class.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
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
