"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy
from scipy import stats
from numbers import Number

from chdir import chdir
from qnorm import qnorm

import pdb


def analyze(A, B, genes, config):
	"""Performs three steps in order: quantile normalize the data, identifies
	differentially expressed genes, and optionally cuts-off or corrects for
	the least significant data points.
	"""

	if len(A) != len(B) != len(genes):
		raise ValueError('Control and experimental expression data and gene \
			symbols must have an equal number of data points')

	if not __all_numbers(A, B):
		raise ValueError('There should be only numbers in control expression \
			data. Non-number element(s) found in ')

	# Quantile normalize the data.
	A, B = qnorm(A, B)

	# Identify differential expression, defaulting to the characteristic
	# direction.
	if config['method'] == 'ttest':
		gene_pvalues = __ttest(A, B, genes, config['cutoff'])
	else:
		gene_pvalues = chdir(A, B, genes, config['cutoff'])
	return gene_pvalues


def __ttest(A, B, genes):
	"""Performs a standard T-test.
	"""

	pvalues = []
	for i in range(len(A)):
		ttest_results = stats.ttest_ind(A[i], B[i])
		# TODO: Ask Andrew if I should use `all()` or `any()`.
		signed_pvalue = ttest_results[1] if (ttest_results[0] > 0).all() else (ttest_results[1] * -1)
		pvalues.append((genes[i], signed_pvalue))

	return pvalues


def __all_numbers(A, B):
	"""Check if there are non-number elements in A or B. We know they are the
	same length at this point.
	"""

	for row in range(len(A)):
		for col in range(len(A[0])):
			if not isinstance(A[row][col], Number):
				return False
			if not isinstance(B[row][col], Number):
				return False
	return True


'''
def __threshold(gene_pvalues, threshold):
	result = []
	for gene, pvalue in gene_pvalues:
		if len(result) > threshold:
			break
		result.append((gene, pvalue))
	pdb.set_trace()
	for  gene, pvalue in reversed(gene_pvalues):
		if len(result) > threshold*2:
			break
		result.append((gene, pvalue))
	return result
'''