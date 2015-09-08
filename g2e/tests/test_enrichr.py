import unittest

from g2e.core.targetapp.enrichr import get_link, convert_ranked_genes_to_tuples, get_genes_as_string
from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene


class TestEnrichr(unittest.TestCase):

    def setUp(self):
        self.ranked_genes = [
            RankedGene(Gene('A'), 1),
            RankedGene(Gene('B'), 1),
            RankedGene(Gene('C'), 1),
            RankedGene(Gene('D'), 1),
            RankedGene(Gene('E'), 1)
        ]

    def testGetLink(self):
        link = get_link(self.ranked_genes, '')
        self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in link)

    # convert_ranked_genes_to_tuples
    def testConvertRankedGenesToTuples(self):
        genes = convert_ranked_genes_to_tuples(self.ranked_genes)
        self.assertEqual(len(genes), len(self.ranked_genes))
        self.assertTrue(type(genes[0]) is tuple)

    def testGetGenesAsString(self):
         genes = convert_ranked_genes_to_tuples(self.ranked_genes)
         gene_str = get_genes_as_string(genes)
         self.assertEqual('1,A\n1,B\n1,C\n1,D\n1,E', gene_str)