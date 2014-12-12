"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy
from scipy import stats

import chdir
import filemanager
from qnorm import quantile_normalize


def analyze(A, B, genes, config):
	"""Performs three steps in order: quantile normalize the data, identifies
	differentially expressed genes, and optionally cuts-off or corrects for
	the least significant data points.
	"""

	if len(A) != len(B) != len(genes):
		ValueError('Control and experimental expression data and gene symbols\
			must have an equal number of data points')

	# Quantile normalize the data. Read more here:
	# http://en.wikipedia.org/wiki/Quantile_normalization
	A, B = quantile_normalize(A, B)

	# Identify differential expression, defaulting to the characteristic
	# direction.
	if config['method'] == 'ttest':
		return __ttest(A, B, genes)
	else:
		return chdir.chdir(A, B, genes)


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