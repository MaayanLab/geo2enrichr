"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dao.util import session_scope
from g2e.model.softfile import SoftFile


def fetch(softfile_name):
    with session_scope() as session:
        tag = session.query(SoftFile).filter_by(name=softfile_name).first()
        return tag