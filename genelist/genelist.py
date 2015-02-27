"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import numpy as np
import os.path

from database import euclid2
from .diffexp import diffexp


class GeneList(object):

	# It is critical that this *preserves order*!
	def __init__(self, A, B, genes, method, cutoff):
		data = diffexp(A, B, genes, method, cutoff)
		self.method = method
		self.cutoff = cutoff
		up = [(t[0],format(t[1],'.6g')) for t in reversed(data) if t[1] > 0 ]
		self.up = {
			'genes': up,
			'link': self.path(up),
			'count': len(up)
		}
		down = [(t[0],format(t[1],'.6g')) for t in data if t[1] < 0 ]
		self.down = {
			'genes': down,
			'link': self.path(down),
			'count': len(down)
		}
		self._write(up, 'up')
		self._write(down, 'down')

	def path(self, data):
		return 'static/genelist/' + self._hash(data) + '.txt'

	def _hash(self, data):
		"""Hashes the 
		"""
		return hashlib.sha1(str(data).encode('utf-8')).hexdigest()

	def _write(self, data, direction):
		if os.path.isfile(self.path(data)):
			return
		with open(self.path(data), 'w+') as f:
			f.write('!method\t' + self.method + '\n')
			f.write('!cutoff\t' + str(self.cutoff) + '\n')
			f.write('!direction\t' + direction + '\n')
			for gene in getattr(self, direction)['genes']:
				f.write(gene[0] + '\t' + gene[1] + '\n')
