"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""


import core.softfile.geodownloader as geodownloader
import core.softfile.softparser as softparser
import core.softfile.normalizer as normalizer
import core.softfile.filemanager as filemanager


class SoftFile(object):

	def __init__(self, name, A_cols=None, B_cols=None, genes=None, A=None, B=None, link=None, is_geo=False, platform=None, stats=None):
		"""Constructs a SOFT file. This should only be called via the class
		methods.
		"""
		self.name = name
		self.A_cols = A_cols
		self.B_cols = B_cols
		self.genes = genes
		self.A = A
		self.B = B
		self.is_geo = is_geo
		self.platform = platform
		self.stats = stats

		self.link = link or filemanager.write(name, genes, A, B)

	@classmethod
	def from_geo(cls, args):
		name = args.get('geo_dataset')
		is_geo = True

		if not filemanager.file_exists(name):
			geodownloader.download(name)

		platform = args['platform']
		A_cols = args['A_cols'].split(',')
		B_cols = args['B_cols'].split(',')
		genes, A, B, stats = softparser.parse_geo(name, platform, A_cols, B_cols)
		genes, A, B = normalizer.normalize(genes, A, B)
		return cls(name, A_cols, B_cols, genes=genes, A=A, B=B, is_geo=is_geo, platform=platform, stats=stats)

	@classmethod
	def from_dao(cls, dao_result):
		softfile = dao_result['softfile']
		name     = softfile['name']
		link     = softfile['link']
		is_geo   = softfile['is_geo']
		platform = softfile['platform']
		return cls(name, platform=platform, link=link, is_geo=is_geo)

	@classmethod
	def from_file(cls, args):
		pass
