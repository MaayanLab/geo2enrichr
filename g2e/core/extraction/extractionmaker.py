"""This module returns an Extraction instance. If given an id, it returns the
extraction from the DAO. Otherwise, it builds a SoftFile and GeneList, saves
them to the DAO and returns a new Extraction.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.core.extraction.extraction import Extraction
from g2e.dao import dao


def extraction_maker(**kwargs):
    """Constructs a single instance of an extraction event.
    """
    if 'id' in kwargs:
        extraction =  dao.fetch(kwargs['id'])
        return clean_extraction(extraction)

    elif 'file' in kwargs:
        extraction = Extraction.from_file(kwargs['file'], kwargs['args'])
        return dao.save(extraction)

    # GEO Dataset
    else:
        extraction = Extraction.from_geo(kwargs['args'])
        print 'extraction created'
        ext_id = dao.save(extraction)
        print 'extraction saved'
        return ext_id


def clean_extraction(extraction):
	"""Removes unnecessary attributes from extraction before returning data to
	the user.
	"""
    response = extraction.__dict__
    response['softfile'] = extraction.softfile.__dict__
    response['genelists'] = [gl.__dict__ for gl in extraction.genelists]
    response['metadata'] = extraction.metadata.__dict__
    # del response['genelists'][0]['ranked_genes']
    # del response['genelists'][1]['ranked_genes']
    # Leave the combined genes?
    #del response['genelists'][2]['ranked_genes']
    del response['softfile']['A']
    del response['softfile']['A_cols']
    del response['softfile']['B']
    del response['softfile']['B_cols']
    del response['softfile']['genes']
    return response
