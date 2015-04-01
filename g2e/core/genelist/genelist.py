"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib

import g2e.core.genelist.genelistfilemanager as filemanager
import g2e.core.genelist.enrichrlink as enrichrlink


class GeneList(object):

    def __init__(self, ranked_genes, direction, metadata, name=None, text_file=None, enrichr_link=None):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.direction    = direction
        self.name         = name or self._name()
        self.text_file    = text_file or filemanager.write(
        	self.name, 
        	self.direction,
        	self.ranked_genes,
        	metadata
        )
        description = self._direction(self.direction) + '_' + str(metadata) 
        # If there is no cutoff, do not send data to Enrichr. The lists will
        # be too big.
        if metadata.cutoff:
            self.enrichr_link = enrichr_link or enrichrlink.get_link(self.ranked_genes, description)
        else:
            self.enrichr_link = ''

    # PURPLE_WIRE: This should handle duplicate file names, although they are
    # unlikely.
    def _name(self):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(self.ranked_genes).encode('utf-8')).hexdigest()

    def _direction(self, direction):
        if direction == 1:
            return 'Up'
        if direction == -1:
            return 'Down'
        return 'Combined'
