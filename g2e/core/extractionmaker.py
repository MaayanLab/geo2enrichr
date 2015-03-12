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
		extraction = Extraction.from_dao(extraction_dao).__dict__
		return extraction

	elif 'file' in kwargs:
		extraction = Extraction.from_file(kwargs['file'], kwargs['args'])
		ex_id = dao.save(extraction)
		return ex_id
	
	# GEO Dataset
	else:
		extraction = Extraction.from_geo(kwargs['args'])
		ex_id = dao.save(extraction)
		return ex_id
