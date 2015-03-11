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
		import pdb; pdb.set_trace()

		args = dao.fetch(kwargs.get('id'))
		extraction = Extraction(args)
		return extraction
	else:
		import pdb; pdb.set_trace()
		args = kwargs.get('args')
		extraction = Extraction(args)
		ex_id = dao.save(extraction)
		return ex_id
