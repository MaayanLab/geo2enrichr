"""Identifies differentially expressed genes. It delegates to the appropriate
method depending on user options and defaults to the characteristic direction.
"""

from g2e.db.utils import get_or_create
from .chdir import chdir
from .ttest import ttest
from substrate import Gene, RankedGene


def diffexp(a_vals, b_vals, genes, metadata):
    """Delegates to the correct helper function based on client or default
    configuration.
    """
    if metadata.diff_exp_method == 'ttest':
        genes, values = ttest(
            a_vals, b_vals, genes,
            metadata.ttest_correction_method,
            metadata.threshold
        )
    else:
        genes, values = chdir(a_vals, b_vals, genes)

    # TODO: We should do this *after* the potential cutoff.
    genes = [get_or_create(Gene, name=name) for name in genes]
    ranked_genes = [RankedGene(pair[0], pair[1]) for pair in zip(genes, values)]
    return ranked_genes
