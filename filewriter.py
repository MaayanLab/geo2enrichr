"""This module handles writing to files.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from files import GeneFile


def output_gene_pvalue_pairs(input_file, gene_pvalue_pairs, inclusion):
	"""Outputs genes and pvalues to file(s) on the server and returns their
	names.
	"""

	input_file  = input_file.replace('.soft', '')
	output_file = GeneFile(input_file + '_' + inclusion)

	import pdb
	pdb.set_trace()

	if inclusion == 'combined':
		with open(output_file.path(), 'w+') as out:
			for gene, pvalue in gene_pvalue_pairs:
				out.write('%s\t%f\n' % (gene, pvalue))

	elif inclusion == 'down':
		with open(output_file.path(), 'w+') as out:
			for gene, pvalue in gene_pvalue_pairs:
				if pvalue < 0:
					out.write('%s\t%f\n' % (gene, pvalue))

	# Default is up genes.
	else:
		with open(output_file.path(), 'w+') as out:
			for gene, pvalue in gene_pvalue_pairs:
				if pvalue > 0:
					out.write('%s\t%f\n' % (gene, pvalue))

	return output_file.filename