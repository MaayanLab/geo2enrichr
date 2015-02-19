import unittest
import numpy as np

from softfile.normalizer import avg_dups


class TestAvgDups(unittest.TestCase):

	def setUp(self):
		self.genes = ['A', 'C', 'C', 'B', 'A']
		self.vals = [
			[2.0, 2.0, 9.0, 9.0],
			[3.0, 3.0, 3.0, 3.0],
			[8.0, 8.0, 2.0, 2.0],
			[4.0, 4.0, 4.0, 3.0],
			[1.0, 1.0, 1.0, 1.0]

		]

	def testLen(self):
		genes, vals = avg_dups(self.genes, self.vals)
		self.assertEqual(len(vals), 3)
		self.assertEqual(len(vals), len(genes))

	def testData(self):
		genes_ans = ['A', 'B', 'C']
		vals_ans  = [
			[1.5, 1.5, 5.0, 5.0],
			[4.0, 4.0, 4.0, 3.0],
			[5.5, 5.5, 2.5, 2.5]
		]

		genes, vals = avg_dups(self.genes, self.vals)
		self.assertTrue(np.array_equal(vals, vals_ans))
		self.assertTrue(np.array_equal(genes, genes_ans))
