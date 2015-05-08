"""This class creates a gene list.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib

import g2e.core.genelist.genelistfilemanager as filemanager
import g2e.core.targetapp.enrichr as enrichr
import g2e.core.targetapp.l1000cds2 as l1000cds2
import g2e.core.targetapp.paea as paea


class GeneList(object):

    def __init__(self, ranked_genes, direction, metadata, name=None, text_file=None, enrichr_link=None, l1000cds2_link=None, paea_link=None):
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

        # If there is no cutoff, do not send data to target APIs. The lists
        # will be too big to handle.
        if metadata.cutoff or metadata.threshold:
            self.enrichr_link = enrichr_link or enrichr.get_link(self.ranked_genes, description)

            # We want to calculate the cosine distance but only for the
            # combined gene list.
            if direction == 0:
                self.l1000cds2_link = l1000cds2_link or l1000cds2.get_link(self.ranked_genes)
                self.paea_link = paea_link or paea.get_link(self.ranked_genes, description)
            else:
                self.l1000cds2_link = ''
                self.paea_link = ''
        else:
            self.enrichr_link = ''
            self.l1000cds2_link = ''
            self.paea_link = ''

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
