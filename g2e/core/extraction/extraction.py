"""This module creates an Extraction instance.
"""


from core.softfile.softfile import SoftFile
from core.genelist.genelist import GeneList
from core.extraction import enrichrlink


class Extraction(object):

	def __init__(self, args):
		"""Construct an Extraction instance.
		"""
		self.softfile = SoftFile.create(args)
		self.method = args.get('method') or 'chdir'
		self.cutoff = args.get('cutoff') or 500
		self.genelist = GeneList.create(self.softfile, self.method, self.cutoff)
		
		up   = [(t[0],str(t[1])) for t in reversed(self.genelist.ranked_genes) if t[1] > 0]
		down = [(t[0],str(t[1])) for t in self.genelist.ranked_genes if t[1] < 0]
		
		self.enrichr_link_up   = enrichrlink.get_link(up, 'up genes')
		self.enrichr_link_down = enrichrlink.get_link(down, 'down genes')

		#self.text_file_up = filewriter.write(up)
		#self.text_file_down = filewriter.write(down)
