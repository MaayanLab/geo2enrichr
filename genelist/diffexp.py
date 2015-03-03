"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from scipy import stats

from . import chdir
from server.log import pprint
import numpy as np


def diffexp(A, B, genes, method, cutoff):
	"""Identifies differentially expressed genes, delegating to the correct
	helper function based on client or default configuration.
	"""
	HALF_CUTOFF = int(cutoff / 2) if cutoff is not 'None' else None
	if method == 'ttest':
		genes, pvalues = ttest(A, B, genes)
		import pdb; pdb.set_trace()
	else:
		pprint('Calculating the characteristic direction.')
		genes, pvalues = chdir.chdir(A, B, genes)

	# Just in case.
	genes = np.array(genes)
	pvalues = np.array(pvalues)

	ind = np.argsort(pvalues)
	genes = genes[ind]
	pvalues = pvalues[ind]
	grouped = [t for t in zip(genes, pvalues)]

	# Apply cutoff; indexing with None is safe.
	return grouped[:HALF_CUTOFF] + grouped[-HALF_CUTOFF:] if HALF_CUTOFF else grouped


def ttest(A, B, genes):
	"""Performs a standard T-test.
	"""

	pvalues = []
	for i in range(len(A)):
		ttest_results = stats.ttest_ind(A[i], B[i])
		# TODO: Ask Andrew if I should use `all()` or `any()`.
		signed_pvalue = ttest_results[1] if (ttest_results[0] > 0).all() else (ttest_results[1] * -1)
		pvalues.append((genes[i], signed_pvalue))

	l = list(zip(*pvalues))
	return l[0], l[1]
