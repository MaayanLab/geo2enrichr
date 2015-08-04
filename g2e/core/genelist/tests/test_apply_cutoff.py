import unittest

from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene
from g2e.core.genelist.genelistsmaker import _apply_cutoff


class TestApplyCutoff(unittest.TestCase):

    def setUp(self):
        self.ranked_genes = [
            RankedGene(Gene('A'), 0.4),
            RankedGene(Gene('B'), 0.6),
            RankedGene(Gene('C'), -0.44),
            RankedGene(Gene('D'), -0.1),
            RankedGene(Gene('E'), 0.2),
            RankedGene(Gene('F'), 0.3)
        ]

    def test_cutoff(self):
        ranked_genes = _apply_cutoff(self.ranked_genes, 4)
        genes = [rg.gene.name for rg in ranked_genes]
        values = [rg.value for rg in ranked_genes]
        self.assertEqual(genes, ['C', 'D', 'E', 'F'])
        self.assertEqual(values, [-0.44, -0.1, 0.2, 0.3])

    def test_no_cutoff(self):
        ranked_genes = _apply_cutoff(self.ranked_genes, None)
        genes = [rg.gene.name for rg in ranked_genes]
        values = [rg.value for rg in ranked_genes]
        self.assertEqual(genes, ['A', 'B', 'C', 'D', 'E', 'F'])
        self.assertEqual(values, [0.4, 0.6, -0.44, -0.1, 0.2, 0.3])
