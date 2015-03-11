"""This module returns an Extraction instance. If given an id, it returns the
extraction from the DAO. Otherwise, it builds a SoftFile and GeneList, saves
them to the DAO and returns a new Extraction.
"""


from core.softfile.softfile import SoftFile
from core.genelist.genelist import GeneList
from core.extraction.extraction import Extraction
from dao import dao


def extraction_maker(**kwargs):
	"""Constructs a single instance of an extraction event.
	"""
	if 'id' in kwargs:
		import pdb; pdb.set_trace()
		extraction = dao.fetch(kwargs.get('id'))
		return extraction
	else:
		args = kwargs.get('args')
		
		softfile = SoftFile.create(args)
		genelist = GeneList.create(softfile, args)
		return dao.save(softfile, genelist)
