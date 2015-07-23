"""Represents a gene list, with references to the list's saved text file and
links to target applications.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib

import g2e.core.genelist.genelistfilemanager as filemanager


class GeneList(object):

    def __init__(self, ranked_genes, direction, metadata, target_apps, name=None, text_file=None):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.direction    = direction
        self.name         = name or self._name()
        self.target_apps  = target_apps
        self.text_file    = text_file or filemanager.write(
            self.name, 
            self.direction,
            self.ranked_genes,
            metadata
        )

    # PURPLE_WIRE: This should handle duplicate file names, although they are
    # unlikely.
    def _name(self):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(self.ranked_genes).encode('utf-8')).hexdigest()