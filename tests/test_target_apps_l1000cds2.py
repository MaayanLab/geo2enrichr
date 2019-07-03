import unittest

import g2e.target_applications.l1000cds2 as l1000cds2
from substrate import Gene, RankedGene, RequiredMetadata


class TestTargetAppsL1000CDS2(unittest.TestCase):

    def test_get_link(self):
        md = RequiredMetadata(None, None, None, None)

        ranked_genes = [
            RankedGene(Gene('DDIT4'), 9.97),
            RankedGene(Gene('HIG2'), 10.16),
            RankedGene(Gene('FLT1'), 7.66),
            RankedGene(Gene('ADM'), 17.8),
            RankedGene(Gene('SLC2A3'), 20.29),
            RankedGene(Gene('ZNF331'), 15.22)
        ]

        link = l1000cds2.get_link(ranked_genes, md)
        self.assertTrue('https://amp.pharm.mssm.edu/L1000CDS2/' in link)