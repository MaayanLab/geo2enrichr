"""Calculates the t-test.

__authors__ = "Gregory Gundersen, Axel Feldman"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
import scipy.stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
r_stats = importr('stats')


def ttest(A, B, genes, ttest_correction_method, ttest_cutoff):
    """Wraps original T-test method, handling sorting by lowest p-value.
    """
    print 'Performing the t-test.'

    genes, pvalues = _get_pvalues(A, B, genes)
    if ttest_correction_method:
        pvalues = _correct_pvalues(pvalues, ttest_correction_method)

    # Zip them together so we can track them.
    gene_pvalues = list(zip(genes, pvalues))

    # Apply cutoff.
    if ttest_cutoff:
        cutoff_pvalues = [x for x in gene_pvalues if abs(x[1]) <= ttest_cutoff]
    else:
        cutoff_pvalues = gene_pvalues

    result = [list(t) for t in zip(*cutoff_pvalues)]
    genes = result[0]
    pvalues = result[1]

    genes, pvalues = _sort_by_lowest_pvalue(genes, pvalues)
    return genes, pvalues


def _get_pvalues(A, B, genes):
    """Performs a standard T-test.
    """
    pvalues = []
    for i in range(len(A)):
        # equal_var=False specifies to use Welch's t-test.
        ttest_results = scipy.stats.ttest_ind(A[i], B[i], equal_var=False)

        # According to SciPy's source code...
        #
        #     https://github.com/scipy/scipy/blob/master/scipy/stats/stats.py
        #
        # ttest_ind(A, B) calculates usig mean(A) - mean(B). This means that
        # if the t-statistic is positive, B has been down regulated. Thus, we
        # give the pvalue a negative sign if ttest_results[0] < 0.
        signed_pvalue = ttest_results[1] if (ttest_results[0] < 0) else (ttest_results[1] * -1)
        pvalues.append(signed_pvalue)

    return genes, pvalues


def _correct_pvalues(pvalues, ttest_correction_method):
    """Corrects for multiple comparisons.
    """
    # The multiple comparisons problem arises when a test increases the
    # the likelihood that an event occurs by testing for it many times. In our
    # case, the t-test is bound to find some differential expression since the
    # test is performed in a univariate fashion; this correction method
    # accounts for that. See here for more information:
	# http://en.wikipedia.org/wiki/Multiple_comparisons_problem
    return r_stats.p_adjust(
        FloatVector(pvalues),
        method = ttest_correction_method
    )


def _sort_by_lowest_pvalue(genes, values):
    """Sorts two lists, one of genes and another of values, by the absolute
    value of the values.
    """
    genes = np.array(genes)
    values = np.array(values)
    ind = np.argsort( np.absolute(values) )
    genes = genes[ind]
    genes = [str(x) for x in genes]
    values = values[ind]
    return list(reversed(genes)), list(reversed(values.tolist()))
