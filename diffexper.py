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
from log import pprint


def analyze(A, B, genes, config, filename=''):
	"""Performs three steps in order:
	1. Quantile normalize the data.
	2. Dentifies differentially expressed genes.
	3. Optionally cuts-off or corrects for the least significant data points.
	"""

	# Verifery the arrays are equal and all numbers.
	__validate(A, B)

	# Quantile normalize the data.
	pprint('Quantile normalizing the data.')
	A, B = qnorm(A, B)
	pprint('Data quantile normalized.')

	# Identify differential expression, defaulting to the characteristic
	# direction.
	if config['method'] == 'ttest':
		gene_pvalues = __ttest(A, B, genes, config['cutoff'])
	else:
		pprint('Calculating the characteristic direction.')
		gene_pvalues = chdir(A, B, genes, config['cutoff'])
		pprint('Characteristic direction calculated.')
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

	# TODO: This should also handle a cutoff.
	return pvalues


def __validate(A, B):
	if len(A) != len(B) != len(genes):
		raise ValueError('Control and experimental expression data and gene \
			symbols must have an equal number of data points.')
	if not __all_numbers(A, B):
		raise ValueError('There should be only numbers in control expression \
			data. Non-number element(s) found.')


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