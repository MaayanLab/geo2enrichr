"""This module handles building the SoftFile and GeneLists, saving them to the
ORM, and returning the appropriate data to the facade.
"""


from core.softfile.softfile import SoftFile
from core.genelist.genelist import GeneList
from orm import orm


def extraction_maker(**kwargs):
	"""Constructs a single instance of an extraction event.
	"""
	if 'id' in kwargs:
		extraction = orm.fetch_extraction(kwargs.get('id'))
		return extraction
	else:
		args = kwargs.get('args')
		softfile = SoftFile.create(args)
		softfile.id = orm.save_softfile(softfile)
		genelist = GeneList.create(softfile, args)
		genelist.id = orm.save_genelist(genelist)
		return orm.save_extraction(softfile.id, genelist.id)
