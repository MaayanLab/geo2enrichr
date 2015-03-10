"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import numpy as np
import os.path

from .diffexp import diffexp
from . import enrichrlink


class GeneList(object):

	# It is critical that this *preserves order*!
	def __init__(self, A, B, genes, method, cutoff):
		"""Constructs a gene list.
		"""
		genes, values = diffexp(A, B, genes, method, cutoff)
		self.ranked_genes = [x for x in zip(reversed(genes), reversed(values))]
		self.method = method
		self.cutoff = cutoff

		up = [(t[0],str(t[1])) for t in reversed(self.ranked_genes) if t[1] > 0 ]
		down = [(t[0],str(t[1])) for t in self.ranked_genes if t[1] < 0 ]
		
		self.enrichr_link_up = enrichrlink.get_link(up, 'up genes')
		self.enrichr_link_down = enrichrlink.get_link(down, 'down genes')

	@classmethod
	def create(cls, softfile, args):
		return cls(softfile.A, softfile.B, softfile.genes, 'chdir', 500)

	def path(self, data):
		return 'static/genelist/' + self._hash(data) + '.txt'

	def _hash(self, data):
		"""Hashes the 
		"""
		return hashlib.sha1(str(data).encode('utf-8')).hexdigest()

	def _write(self, data, direction):
		if os.path.isfile(self.path(data)):
			print('Gene list file already created')
			return
		with open(self.path(data), 'w+') as f:
			f.write('!method\t' + self.method + '\n')
			f.write('!cutoff\t' + str(self.cutoff) + '\n')
			f.write('!direction\t' + direction + '\n')
			for gene in getattr(self, direction)['genes']:
				f.write(gene[0] + '\t' + gene[1] + '\n')
