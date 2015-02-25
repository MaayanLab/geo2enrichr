"""
"""


import numpy as np
import os.path

from server.log import pprint
from .geodownloader import download
from .parser import parse
from .normalizer import normalize


class SoftFile(object):

	def __init__(self, name=None, genes=None, A=None, B=None, stats=None):
		self.name = name
		self.genes = genes
		self.A = A
		self.B = B
		self.stats = stats
		AB = self.concat(A, B)
		self._write(self.name, self.genes, AB)
		self.link = self.path(name, True)

	@classmethod
	def from_geo(cls, dataset, platform, A_cols, B_cols, norm=True):
		name = dataset
		#self.platform = platform
		#self.gsms = A_cols + B_cols
			
		if not os.path.isfile(cls.path(name)):
			# This function writes a file to disk; the file's location can be
			# found at self.path().
			download(self.name, cls.path(name))
		
		genes, A, B, stats = parse(cls.path(name), platform, A_cols, B_cols)
		AB = cls.concat(A, B)
		if norm:
			idx = len(A[0])
			genes, AB = normalize(np.array(genes), AB)
			genes = genes.tolist()
			A = AB[:,:idx].tolist()
			B = AB[:,idx:].tolist()

		return cls(name, genes, A, B, stats)

	@classmethod
	def from_string(cls, string):
		lines = string.split('\n')
		names = lines[0].split('\t')[1:]
		samples = lines[1].split('\t')[1:]
		A_indices = [i for (i,x) in enumerate(samples) if x == '0']
		B_indices = [i for (i,x) in enumerate(samples) if x == '1']
		genes = []
		A = []
		B = []
		for line in lines[2:]:
			line = line.split('\t')
			genes.append( line[0] )
			line = line[1:]
			A.append([ float(line[i]) for i in A_indices ])
			B.append([ float(line[i]) for i in B_indices ])
		lines = lines[2:]

		return cls('TODO', genes=genes, A=A, B=B)

	@classmethod
	def path(cls, name, clean=False):
		if clean:
			return 'static/soft/clean/' + name + '.soft'
		return 'static/soft/' + name + '.soft'

	@classmethod
	def concat(cls, A, B):
		return np.concatenate((A, B), axis=1)

	#def clean_path(self, name):
	#	#return 'static/soft/clean/' + name + '-'.join(gsms) + '.soft'
	#	return 'static/soft/clean/' + name + '.soft'

	def _write(self, name, genes, values):
		gene_values_dict = { k:v for (k,v) in zip(genes, values) }
		if os.path.isfile(self.path(name, True)):
			return

		pprint('Writing clean SOFT file.')
		with open(self.path(name, True), 'w+') as f:
			f.write('!datset\t' + self.name + '\n')
			#f.write('!platform\t' + self.platform + '\n')
			#f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
			#f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
			f.write('!end_metadata\n')
			#f.write('GENE SYMBOL\t' + '\t'.join(self.gsms) + '\n')
			for gene, val in gene_values_dict.items():
				val_str = '\t'.join(map(str, val))
				f.write(gene + '\t' + val_str + '\n')
