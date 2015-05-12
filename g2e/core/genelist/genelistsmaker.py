"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
import os.path

from g2e.core.genelist.diffexp import diffexp
from g2e.core.genelist.genelist import GeneList
from g2e.core.targetapp.targetapps import target_all_apps 


def genelists_maker(softfile, metadata):
    """Wrapper method for creating one of each "kind" of gene list: up, down,
    and combined.
    """
    # 1. Perform differential expression analysis with no cutoff. We do
    #    perform the thresholding for the t-test since that is part of
    #    the analysis.
    genes, values = diffexp(
        softfile.A,
        softfile.B,
        softfile.genes,
        metadata
    )

    # 2. Analyze the full gene list on target applications.
    #    "f_" prefix stands for "full".
    f_ranked_genes = zip(genes, values)
    f_up_genes     = [t for t in f_ranked_genes if t[1] > 0]
    f_down_genes   = [t for t in f_ranked_genes if t[1] < 0]

    target_apps_up       = target_all_apps(f_up_genes,     1, metadata)
    target_apps_down     = target_all_apps(f_down_genes,  -1, metadata)
    target_apps_combined = target_all_apps(f_ranked_genes, 0, metadata)

    # 3. Apply cutoff if the differential expression method is the
    #    Characteristic Direction. We don't apply it earlier because PAEA
    #    requires the full signature.
    if metadata.diffexp_method == 'chdir':
        print 'Applying cutoff to the Characteristic Direction'
        genes, values = _apply_cutoff(genes, values, metadata.cutoff)

    # 4. Build gene lists that we will store.

    # numpy sorts the data from left-to-right, but we render the results
    # "top-to-bottom", meaning we need to reverse the lists.
    ranked_genes = list(zip(reversed(genes), reversed(values)))
    up_genes     = [t for t in ranked_genes if t[1] > 0]
    down_genes   = [t for t in ranked_genes if t[1] < 0]
    genelists = [
        GeneList(up_genes,     1, metadata, target_apps_up),
        GeneList(down_genes,  -1, metadata, target_apps_down),
        GeneList(ranked_genes, 0, metadata, target_apps_combined)
    ]

    return genelists


def _apply_cutoff(genes, values, cutoff):
    """Applies a cutoff to both lists, assuming left-to-right
    least-to-greatest.
    """
    if cutoff is None:
        return genes, values
    return genes[-cutoff:], values[-cutoff:]
