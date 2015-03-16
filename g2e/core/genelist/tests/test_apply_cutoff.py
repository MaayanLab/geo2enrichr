import unittest
import numpy as np

from core.genelist.diffexp import _apply_cutoff


class TestApplyCutoff(unittest.TestCase):

    def setUp(self):
        self.genes  = ['A', 'B', 'C', 'D', 'E', 'F']
        self.values = [0.4, 0.6, -0.44, -0.1, 0.2, 0.3]

    def test_cutoff(self):
        genes, values = _apply_cutoff(self.genes, self.values, 4)
        self.assertEqual(genes, ['C', 'D', 'E', 'F'])
        self.assertEqual(values, [-0.44, -0.1, 0.2, 0.3])

    def test_no_cutoff(self):
        genes, values = _apply_cutoff(self.genes, self.values, None)
        self.assertEqual(genes, ['A', 'B', 'C', 'D', 'E', 'F'])
        self.assertEqual(values, [0.4, 0.6, -0.44, -0.1, 0.2, 0.3])
