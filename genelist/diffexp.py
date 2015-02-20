"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from scipy import stats

import chdir
from server.log import pprint


def diffexp(A, B, genes, method, cutoff):
	"""Identifies differentially expressed genes, delegating to the correct
	helper function based on client or default configuration.
	"""
	HALF_CUTOFF = cutoff / 2 if cutoff is not 'None' else None
	if method == 'ttest':
		gene_pvalues = ttest(A, B, genes)
	else:
		pprint('Calculating the characteristic direction.')
		genes, pvalues = chdir.chdir(A, B, genes)

	# Notice we return the unmodified pvalue, *not* the absolute pvalue.
	grouped = zip([abs(pv) for pv in pvalues], genes, pvalues)
	grouped = sorted(grouped, key=lambda item: item[0], reverse=True)

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

	# TODO: This should also handle a cutoff.
	return pvalues
