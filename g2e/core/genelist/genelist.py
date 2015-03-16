"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import numpy as np
import os.path

from core.genelist.diffexp import diffexp
import core.genelist.genelistfilemanager as genelistfilemanager


class GeneList(object):

    def __init__(self, ranked_genes, text_file):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.text_file = text_file

    @classmethod
    def new(cls, softfile, method, cutoff):
        genes, values = diffexp(softfile.A, softfile.B, softfile.genes, method, cutoff)
        # numpy sorts the data from left-to-right, but we render the results
        # "top-to-bottom", meaning we need to reverse the lists.
        genes = reversed(genes)
        values = reversed(values)
        ranked_genes = list(zip(genes, values))
        filename = cls._hash(ranked_genes)
        # The filemanager will handle duplicate filenames and return a full
        # link to the file on the server.
        text_file = genelistfilemanager.write(filename, ranked_genes)
        return cls(ranked_genes, text_file)

    @classmethod
    def from_dao(cls, gl_dao):
        ranked_genes = gl_dao['ranked_genes']
        text_file    = gl_dao['text_file']
        return cls(ranked_genes, text_file)

    @classmethod
    def _hash(cls, data):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(data).encode('utf-8')).hexdigest()
