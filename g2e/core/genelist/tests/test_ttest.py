import unittest
import numpy as np

from g2e.core.genelist.ttest import _sort_by_lowest_pvalue


class TestTtest(unittest.TestCase):


    def test_sort(self):
        genes, values = _sort_by_lowest_pvalue(
            ['A', 'B', 'C', 'D', 'E', 'F'],
            [0.4, 0.6, -0.44, -0.1, 0.2, 0.3]
        )
        self.assertEqual(genes, ['B', 'C', 'A', 'F', 'E', 'D'])
        self.assertEqual(values, [0.6, -0.44, 0.4, 0.3, 0.2, -0.1])
