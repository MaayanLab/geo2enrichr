"""This module handles reading and writing SoftFiles to disk.
"""


import os.path

import core.softfile.normalizer as normalizer


def write(name, genes, A, B):
	"""Writes the contents of a SoftFile to disk and returns a relative path.
	"""
	AB = normalizer.concat(A, B)
	gene_values_dict = { k:v for (k,v) in zip(genes, AB) }
	if not os.path.isfile(path(name, 'clean')):
		print('Writing clean SOFT file.')
		with open(path(name, 'clean'), 'w+') as f:
			f.write('!datset\t' + name + '\n')
			#f.write('!platform\t' + self.platform + '\n')
			#f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
			#f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
			f.write('!end_metadata\n')
			#f.write('GENE SYMBOL\t' + '\t'.join(self.gsms) + '\n')
			for gene, val in gene_values_dict.items():
				val_str = '\t'.join(map(str, val))
				f.write(gene + '\t' + val_str + '\n')
	return path(name, 'clean')


def save(name, file_obj):
	"""
	"""
	full_path =  path(name)
	file_obj.save(full_path)
	return full_path


def file_exists(name):
	"""Returns True if the SoftFile exists on the server, False otherwise.
	"""
	if os.path.isfile(path(name)):
		return True
	return False


def path(name, subdir=None):
	"""Returns a relative path to the SoftFile on the server.
	"""
	subdir = subdir + '/' if subdir else ''
	return 'static/softfile/' + subdir + name + '.soft'
