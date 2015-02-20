"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from diffexp import diffexp


class GeneList(object):

	def __init__(self, A, B, genes, method, cutoff):
		gene_pvalues = diffexp(A, B, genes, method, cutoff)
		self.gene_pvalues = { x[0]:x[1] for x in gene_pvalues }
