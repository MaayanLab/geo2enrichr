"""Handles fetching GeneLists based on name.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.dao.util import session_scope
from g2e.model.genelist import GeneList


def fetch(genelist_name):
    """Single entry point for fetching extractions from database by ID.
    """
    print 'Fetching GeneList ' + genelist_name
    with session_scope() as session:
        genelist = session.query(GeneList).filter_by(name=genelist_name).first()
        return genelist