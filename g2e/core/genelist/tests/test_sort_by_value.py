import unittest

from core.genelist.diffexp import _sort_by_value


class TestSortByValue(unittest.TestCase):

    def setUp(self):
        self.genes  = ['A', 'B', 'C', 'D', 'E', 'F']
        self.values = [0.4, 0.6, -0.44, -0.1, 0.2, 0.3]

    def test_sort(self):
        genes, values = _sort_by_value(self.genes, self.values)
        self.assertEqual(genes, ['D', 'E', 'F', 'A', 'C', 'B'])
        self.assertEqual(values, [-0.1, 0.2, 0.3, 0.4, -0.44, 0.6])
