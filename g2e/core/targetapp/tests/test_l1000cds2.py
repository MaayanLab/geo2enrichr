import unittest

import g2e.core.targetapp.l1000cds2 as l1000cds2
from g2e.core.metadata.metadata import Metadata
from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene


class TestL1000CDS2(unittest.TestCase):

    def testL1000CDS2Link(self):
        md = Metadata(None, None, None, None, None, None, None, None, None)

        ranked_genes = [
            RankedGene(Gene('DDIT4'), 9.97),
            RankedGene(Gene('HIG2'), 10.16),
            RankedGene(Gene('FLT1'), 7.66),
            RankedGene(Gene('ADM'), 17.8),
            RankedGene(Gene('SLC2A3'), 20.29),
            RankedGene(Gene('ZNF331'), 15.22)
        ]

        link = l1000cds2.get_link(ranked_genes, md)
        self.assertTrue('http://amp.pharm.mssm.edu/L1000CDS2/' in link)