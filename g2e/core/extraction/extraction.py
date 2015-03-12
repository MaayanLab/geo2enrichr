"""This module creates an Extraction instance.
"""


from core.softfile.softfile import SoftFile
from core.genelist.genelist import GeneList
from core.extraction import enrichrlink


class Extraction(object):

	def __init__(self, softfile, genelist, method, cutoff, softfile_link, enrichr_link_up, enrichr_link_down):
		"""Construct an Extraction instance.
		"""
		self.softfile = softfile
		self.genelist = genelist
		self.method   = method
		self.cutoff   = cutoff
		self.softfile_link     = softfile_link
		self.enrichr_link_up   = enrichr_link_up
		self.enrichr_link_down = enrichr_link_down

	@classmethod
	def from_geo(cls, args):
		softfile = SoftFile.from_geo(args)
		method   = args.get('method') or 'chdir'
		cutoff   = args.get('cutoff') or 500
		genelist = GeneList.create(softfile, method, cutoff)
		up       = [(t[0],str(t[1])) for t in reversed(genelist.ranked_genes) if t[1] > 0]
		down     = [(t[0],str(t[1])) for t in genelist.ranked_genes if t[1] < 0]
		enrichr_link_up   = enrichrlink.get_link(up, 'up genes')
		enrichr_link_down = enrichrlink.get_link(down, 'down genes')
		return cls(softfile, genelist, method, cutoff, softfile.link, enrichr_link_up, enrichr_link_down)

	@classmethod
	def from_dao(cls, extraction_dao):
		softfile = SoftFile.from_dao(extraction_dao)
		genelist = extraction_dao['genelist']
		method   = extraction_dao['method']
		cutoff   = extraction_dao['cutoff']
		enrichr_link_up   = extraction_dao['enrichr_link_up']
		enrichr_link_down = extraction_dao['enrichr_link_down']
		return cls(softfile.name, genelist, method, cutoff, softfile.link, enrichr_link_up, enrichr_link_down)

	@classmethod
	def from_file(cls, args):
		softfile = SoftFile.from_file(args)
