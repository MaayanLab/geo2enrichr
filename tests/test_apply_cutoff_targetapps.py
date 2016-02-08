import unittest

from g2e.targetapps.maker import _apply_cutoff


class TestApplyCutoff(unittest.TestCase):

    def setUp(self):
        self.ranked_genes = [
            ('A', 0.4),
            ('B', 0.6),
            ('C', -0.44),
            ('D', -0.1),
            ('E', 0.2),
            ('F', 0.3)
        ]

    def test_cutoff(self):
        ranked_genes = _apply_cutoff(self.ranked_genes, 4)
        self.assertEqual(ranked_genes, [
            ('C', -0.44),
            ('D', -0.1),
            ('E', 0.2),
            ('F', 0.3)
        ])
