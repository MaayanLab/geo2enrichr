"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os.path

from diffexp import diffexp


class GeneList(object):

	def __init__(self, A, B, genes, method, cutoff):
		self.data = diffexp(A, B, genes, method, cutoff)
		self.method = method
		# The same ordered list of genes will produce the same hash.
		self.name = str(hash(''.join(genes)))
		self.cutoff = cutoff
		self._write()
		self.link = self.path()

	def path(self):
		return 'static/genelist/' + self.name + '.txt'

	def _write(self):
		if os.path.isfile(self.path()):
			return
		with open(self.path(), 'w+') as f:
			f.write('!method\t' + self.method + '\n')
			f.write('!cutoff\t' + self.cutoff + '\n')
			for gene in self.data:
				f.write(gene + '\t' + str(self.data[gene]) + '\n')
