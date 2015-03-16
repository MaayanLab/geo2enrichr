"""This module creates an Extraction instance.
"""


from core.softfile.softfile import SoftFile
from core.genelist.genelist import GeneList
from core.extraction import enrichrlink


class Extraction(object):

	def __init__(self, softfile, genelist, method, cutoff, enrichr_link_up, enrichr_link_down):
		"""Construct an Extraction instance. This is called only by class
		methods.
		"""
		self.softfile           = softfile
		self.genelist           = genelist
		self.method             = method
		self.cutoff             = cutoff
		self.enrichr_link_up    = enrichr_link_up
		self.enrichr_link_down  = enrichr_link_down

	@classmethod
	def new(cls, softfile, args):
		method   = args['method'] if 'method' in args else 'chdir'
		cutoff   = args['cutoff'] if 'cutoff' in args else 500
		if cutoff == 'None':
			cutoff = None
		genelist = GeneList.new(softfile, method, cutoff)
		up       = [(t[0], str(t[1])) for t in genelist.ranked_genes if t[1] > 0]
		# Enrichr does not care about the sign of the rank; it treats the rank
		# simply as a membership value for a fuzzy set.
		down     = [(t[0], str(-1 * t[1])) for t in genelist.ranked_genes if t[1] < 0]
		enrichr_link_up   = enrichrlink.get_link(up, 'up genes')
		enrichr_link_down = enrichrlink.get_link(down, 'down genes')
		return cls(softfile, genelist, method, cutoff, enrichr_link_up, enrichr_link_down)

	@classmethod
	def from_geo(cls, args):
		softfile = SoftFile.from_geo(args)
		return cls.new(softfile, args)

	@classmethod
	def from_file(cls, file_obj, args):
		# PURPLE_WIRE: Users *will* upload bad data and parsing their files
		# *will* throw an error. Catch and handle appropriately.
		softfile = SoftFile.from_file(file_obj, args)
		return cls.new(softfile, args)

	@classmethod
	def from_dao(cls, ext_dao):
		softfile = SoftFile.from_dao( ext_dao['softfile'] )
		genelist = GeneList.from_dao( ext_dao['genelist'] )
		method   = ext_dao['method']
		cutoff   = ext_dao['cutoff']
		enrichr_link_up   = ext_dao['enrichr_link_up']
		enrichr_link_down = ext_dao['enrichr_link_down']
		return cls(softfile, genelist, method, cutoff, enrichr_link_up, enrichr_link_down)
