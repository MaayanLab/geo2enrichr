"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""


import os.path
import numpy as np

from orm import orm
from .geodownloader import download
from . import softparser
from .normalizer import normalize


class SoftFile(object):

	def __init__(self, name, samples, genes, A, B, is_geo=False, platform=None, stats=None):
		"""Constructs a SOFT file.
		"""
		self.name = name
		self.samples = samples
		self.genes = genes
		self.A = A
		self.B = B
		self.is_geo = is_geo
		self.platform = platform
		self.stats = stats
		self.id = orm.save_softfile(self)

	@classmethod
	def create(cls, args):
		if 'geo_dataset' in args:
			name = args.get('geo_dataset')
			is_geo = True

			if not os.path.isfile(cls.path(name)):
				download(name, cls.path(name))

			platform = args.get('platform')
			A_cols = args.get('A_cols').split(',')
			B_cols = args.get('B_cols').split(',')
			samples = A_cols + B_cols

			genes, A, B, stats = softparser.parse_geo(cls.path(name), platform, A_cols, B_cols)
			AB = cls.concat(A, B)
			
			idx = len(A[0])
			genes, AB = normalize(np.array(genes), AB)
			genes = genes.tolist()
			A = AB[:,:idx].tolist()
			B = AB[:,idx:].tolist()

			return cls(name, samples, genes, A, B, is_geo, platform, stats)

		else:
			# Construct from file
			pass

	@classmethod
	def path(cls, name, clean=False):
		if clean:
			return 'static/softfile/clean/' + name + '.soft'
		return 'static/softfile/' + name + '.soft'

	@classmethod
	def from_geo(cls, dataset, platform, A_cols, B_cols, norm=True):
		"""Delegates to __init__ after downloading, parsing, and normalizing
		data from GEO.
		"""
		name = dataset
		samples = A_cols + B_cols
			
		if not os.path.isfile(cls.path(name)):
			# This function writes a file to disk; the file's location can be
			# found at self.path().
			download(name, cls.path(name))
		
		if norm:
			idx = len(A[0])
			genes, AB = normalize(np.array(genes), AB)
			genes = genes.tolist()
			A = AB[:,:idx].tolist()
			B = AB[:,idx:].tolist()

		return cls(name, samples, genes, A, B, platform, stats)

	# This semlls.
	@classmethod
	def concat(cls, A, B):
		return np.concatenate((A, B), axis=1)


	@classmethod
	def fetch(cls, extraction_id):
		pass

	






	'''
	@classmethod
	def from_file(cls, name, file_obj, platform=None):
		"""Delegates to __init__ after handling a user's custom SOFT file.
		"""
		# Prevent collisions in user file names.
		if os.path.isfile(cls.path(name)):
			name += str(time())[10:]

		file_obj.save(cls.path(name))
		genes, samples, header, A, B = softparser.parse_custom(cls.path(name))
		return cls(name, samples, genes, A, B, platform, pairs=[x for x in zip(samples, header)])

	@classmethod
	def from_example(cls):
		"""Delegates to __init__ after parsing the example file on the server.
		"""
		genes, samples, header, A, B = softparser.parse_custom(cls.path('example'))
		return cls('example', samples, genes, A, B)


	def _write(self, name, genes, values):
		gene_values_dict = { k:v for (k,v) in zip(genes, values) }
		if os.path.isfile(self.path(name, True)):
			return

		pprint('Writing clean SOFT file.')
		with open(self.path(name, True), 'w+') as f:
			f.write('!datset\t' + self.name + '\n')
			if self.platform:
				f.write('!platform\t' + self.platform + '\n')
			if self.stats:
				f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
				f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
			f.write('!end_metadata\n')
			f.write('GENE SYMBOL\t' + '\t'.join(self.samples) + '\n')
			for gene, val in gene_values_dict.items():
				val_str = '\t'.join([format(n,'.4g') for n in val])
				f.write(gene + '\t' + val_str + '\n')'''
