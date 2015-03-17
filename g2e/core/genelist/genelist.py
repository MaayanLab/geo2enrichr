"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import requests

import core.genelist.genelistfilemanager as filemanager
import core.genelist.enrichrlink as enrichrlink


class GeneList(object):

    def __init__(self, ranked_genes, direction, name=None, text_file=None, enrichr_link=None):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.direction    = direction
        self.name         = name or self._name()
        self.text_file    = text_file or filemanager.write(self.name, self.ranked_genes)
        self.enrichr_link = enrichr_link or enrichrlink.get_link(self.ranked_genes)

    # PURPLE_WIRE: This should handle duplicate file names, although they are
    # unlikely.
    def _name(self):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(self.ranked_genes).encode('utf-8')).hexdigest()
