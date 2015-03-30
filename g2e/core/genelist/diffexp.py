"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.core.genelist import chdir
from g2e.core.genelist import ttest


def diffexp(A, B, genes, method, cutoff):
    """Identifies differentially expressed genes, delegating to the correct
    helper function based on client or default configuration.
    """
    if method == 'ttest':
        genes, values = ttest.ttest(A, B, genes)
    else:
    	genes, values = chdir.chdir(A, B, genes)

    genes, values = _apply_cutoff(genes, values, cutoff)
    return genes, values


def _apply_cutoff(genes, values, cutoff):
    """Applies a cutoff to both lists.
    """
    if cutoff is None:
        return genes, values
    return genes[-cutoff:], values[-cutoff:]
