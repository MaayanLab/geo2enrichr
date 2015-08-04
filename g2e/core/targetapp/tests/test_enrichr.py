import unittest

import g2e.core.targetapp.enrichr as enrichr
from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene


class TestEnrichr(unittest.TestCase):

    def testEnrichrLink(self):
        ranked_genes = [
            RankedGene(Gene('A'), 1),
            RankedGene(Gene('B'), 1),
            RankedGene(Gene('C'), 1),
            RankedGene(Gene('D'), 1),
            RankedGene(Gene('E'), 1)
        ]
        link = enrichr.get_link(ranked_genes, '')
        self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in link)
