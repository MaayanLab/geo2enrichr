"""Identifies differentially expressed genes. It delegates to the appropriate
method depending on user options and defaults to the characteristic direction.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.core.genelist import chdir
from g2e.core.genelist import ttest
from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene
from g2e.dataaccess.util import get_or_create


def diffexp(a_vals, b_vals, genes, metadata):
    """Delegates to the correct helper function based on client or default
    configuration.
    """
    if metadata.diff_exp_method == 'ttest':
        genes, values = ttest.ttest(
            a_vals, b_vals, genes,
            metadata.ttest_correction_method,
            metadata.threshold
        )
    else:
        genes, values = chdir.chdir(a_vals, b_vals, genes)

    # TODO: We should do this *after* the potential cutoff.
    genes = [get_or_create(Gene, name=name) for name in genes]
    ranked_genes = [RankedGene(pair[0], pair[1]) for pair in zip(genes, values)]
    return ranked_genes
