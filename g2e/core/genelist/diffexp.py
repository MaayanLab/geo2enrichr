"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from scipy import stats

from core.genelist import chdir
import numpy as np


def diffexp(A, B, genes, method, cutoff):
    """Identifies differentially expressed genes, delegating to the correct
    helper function based on client or default configuration.
    """
    if method == 'ttest':
        genes, values = ttest(A, B, genes)
    else:
        print('Calculating the characteristic direction.')
        genes, values = chdir.chdir(A, B, genes)
    genes, values = _sort_by_value(genes, values)
    genes, values = _apply_cutoff(genes, values, cutoff)
    return genes, values


def ttest(A, B, genes):
    """Performs a standard T-test.
    """
    values = []
    for i in range(len(A)):
        ttest_results = stats.ttest_ind(A[i], B[i])
        # TODO: Ask Andrew if I should use `all()` or `any()`.
        signed_pvalue = ttest_results[1] if (ttest_results[0] > 0).all() else (ttest_results[1] * -1)
        values.append((genes[i], signed_pvalue))

    l = list(zip(*values))
    return l[0], l[1]


def _sort_by_value(genes, values):
    """Sorts two lists, one of genes and another of values, by the absolute
    value of the values.
    """
    genes = np.array(genes)
    values = np.array(values)
    ind = np.argsort( np.absolute(values) )
    genes = genes[ind]
    genes = [str(x) for x in genes]
    values = values[ind]
    return genes, values.tolist()


# http://amp.pharm.mssm.edu/jira/browse/GE-33
# http://amp.pharm.mssm.edu/jira/browse/GE-34
def _apply_cutoff(genes, values, cutoff):
    """Applies a cutoff to both lists.
    """
    if cutoff is None:
        return genes, values
    return genes[-cutoff:], values[-cutoff:]
