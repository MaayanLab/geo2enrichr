"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import numpy as np
import os.path

from core.genelist.diffexp import diffexp


class GeneList(object):

    # It is critical that this *preserves order*!
    def __init__(self, A, B, genes, method, cutoff):
        """Constructs a gene list.
        """
        genes, values = diffexp(A, B, genes, method, cutoff)
        self.ranked_genes = [x for x in zip(reversed(genes), reversed(values))]

    @classmethod
    def create(cls, softfile, method, cutoff):
        return cls(softfile.A, softfile.B, softfile.genes, method, cutoff)

    def path(self, data):
        return 'static/genelist/' + self._hash(data) + '.txt'

    def _hash(self, data):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(data).encode('utf-8')).hexdigest()
