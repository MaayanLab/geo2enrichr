"""This code calculates the t-test.

__authors__ = "Gregory Gundersen, Axel Feldman"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
from scipy import stats


def ttest(A, B, genes):
    """Wraps original T-test method, handling sorting by lowest p-value.
    """
    print 'Performing the t-test.'
    genes, values = _ttest(A, B, genes)
    genes, values = _sort_by_lowest_pvalue(genes, values)
    return genes, values


def _ttest(A, B, genes):
    """Performs a standard T-test.
    """
    values = []
    for i in range(len(A)):
        ttest_results = stats.ttest_ind(A[i], B[i])
        signed_pvalue = ttest_results[1] if (ttest_results[0] > 0) else (ttest_results[1] * -1)
        values.append((genes[i], signed_pvalue))

    l = list(zip(*values))
    return l[0], l[1]


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
    return genes[::-1], values.tolist()[::-1]
