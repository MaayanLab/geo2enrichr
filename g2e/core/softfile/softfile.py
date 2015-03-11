"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""


import os.path
import numpy as np

import core.softfile.geodownloader as geodownloader
import core.softfile.softparser as softparser
import core.softfile.normalizer as normalizer


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

	@classmethod
	def create(cls, args):
		if 'geo_dataset' in args:
			name = args.get('geo_dataset')
			is_geo = True

			if not os.path.isfile(cls.path(name)):
				geodownloader.download(name, cls.path(name))

			platform = args.get('platform')
			A_cols = args.get('A_cols').split(',')
			B_cols = args.get('B_cols').split(',')
			samples = A_cols + B_cols

			genes, A, B, stats = softparser.parse_geo(cls.path(name), platform, A_cols, B_cols)
			AB = cls.concat(A, B)
			
			idx = len(A[0])
			genes, AB = normalizer.normalize(np.array(genes), AB)
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
	def concat(cls, A, B):
		return np.concatenate((A, B), axis=1)
