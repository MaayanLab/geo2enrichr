"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
import os.path

from g2e.core.genelist.diffexp import diffexp
from g2e.core.genelist.genelist import GeneList


def genelists_maker(softfile, metadata):
    genes, values = diffexp(
        softfile.A,
        softfile.B,
        softfile.genes,
        metadata.method,
        metadata.cutoff
    )
    # numpy sorts the data from left-to-right, but we render the results
    # "top-to-bottom", meaning we need to reverse the lists.
    ranked_genes = list(zip(reversed(genes), reversed(values)))
    
    genelists  = []
    up_genes   = [t for t in ranked_genes if t[1] > 0]
    down_genes = [t for t in ranked_genes if t[1] < 0]

    genelists.append( GeneList(up_genes, 1, metadata=metadata) )
    genelists.append( GeneList(down_genes, -1, metadata=metadata) )
    genelists.append( GeneList(ranked_genes, 0, metadata=metadata) )

    return genelists
