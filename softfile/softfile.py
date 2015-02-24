"""
"""


import numpy as np
import os.path

from server.log import pprint
from .geodownloader import download
from .parser import parse
from .normalizer import normalize


class SoftFile(object):

	def __init__(self, dataset, platform, A_cols, B_cols, norm=True):
		self.dataset = dataset
		self.platform = platform
		self.gsms = A_cols + B_cols
			
		if not os.path.isfile(self.path()):
			# This function writes a file to disk; the file's location can be
			# found at self.path().
			download(self.dataset, self.path())
		
		genes, A, B, self.stats = parse(self.path(), self.platform, A_cols, B_cols)
		AB = np.concatenate((A, B), axis=1)
		if norm:
			idx = len(A[0])
			genes, AB = normalize(np.array(genes), AB)
			self.genes = genes.tolist()
			self.A = AB[:,:idx].tolist()
			self.B = AB[:,idx:].tolist()
		else:
			self.genes = genes
			self.A = A
			self.B = B
			
		self._write(self.genes, AB)
		self.link = self.clean_path()

	def path(self):
		return 'static/soft/' + self.dataset + '.soft'

	def clean_path(self):
		return 'static/soft/clean/' + self.dataset + '-'.join(self.gsms) + '.soft'

	def _write(self, genes, values):
		gene_values_dict = { k:v for (k,v) in zip(genes, values) }
		if os.path.isfile(self.clean_path()):
			return

		pprint('Writing clean SOFT file.')
		with open(self.clean_path(), 'w+') as f:
			f.write('!datset\t' + self.dataset + '\n')
			f.write('!platform\t' + self.platform + '\n')
			f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
			f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
			f.write('!end_metadata\n')
			f.write('GENE SYMBOL\t' + '\t'.join(self.gsms) + '\n')
			for gene, val in gene_values_dict.items():
				val_str = '\t'.join(map(str, val))
				f.write(gene + '\t' + val_str + '\n')
