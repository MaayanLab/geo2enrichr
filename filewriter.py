"""This module handles writing to files.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from files import GeneFile


def output_gene_pvalue_pairs(input_file, gene_pvalue_pairs):
	"""Outputs genes and pvalues to file(s) on the server and returns their
	names.
	"""

	input_file  = input_file.replace('.soft', '')
	up_file = GeneFile(input_file + '_' + 'up')
	down_file = GeneFile(input_file + '_' + 'down')
	enrichr_file = GeneFile(input_file + '_' + 'enrichr')

	with open(up_file.path(), 'w+') as up_out, open(down_file.path(), 'w+') as down_out,  open(enrichr_file.path(), 'w+') as enrichr_out:
		for gene, pvalue in gene_pvalue_pairs:
			if pvalue > 0:
				up_out.write('%s\t%f\n' % (gene, pvalue))
			if pvalue < 0:
				down_out.write('%s\t%f\n' % (gene, pvalue))
			# We have already sorted the pvalues by absolute value. Just take
			# it again to remove the sign.
			enrichr_out.write('%s\t%f\n' % (gene, abs(pvalue)))

	return {
		'up': up_file.filename,
		'down': down_file.filename,
		'enrichr': enrichr_file.filename
	}