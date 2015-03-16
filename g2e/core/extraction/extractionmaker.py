"""This module returns an Extraction instance. If given an id, it returns the
extraction from the DAO. Otherwise, it builds a SoftFile and GeneList, saves
them to the DAO and returns a new Extraction.
"""


from core.extraction.extraction import Extraction
from dao import dao


def extraction_maker(**kwargs):
    """Constructs a single instance of an extraction event.
    """
    if 'id' in kwargs:
        extraction_dao = dao.fetch(kwargs['id'])
        return Extraction.from_dao(extraction_dao)

    elif 'file' in kwargs:
        extraction = Extraction.from_file(kwargs['file'], kwargs['args'])
        return dao.save(extraction)
    
    # GEO Dataset
    else:
        extraction = Extraction.from_geo(kwargs['args'])
        return dao.save(extraction)
