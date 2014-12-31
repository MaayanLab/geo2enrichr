import unittest
import numpy as np

from cleaner import avg_dups


class TestAvgDups(unittest.TestCase):


	def setUp(self):
		self.genes = ['A', 'C', 'C', 'B', 'A']
		self.A = [
			[2.0, 2.0],
			[3.0, 3.0],
			[8.0, 8.0],
			[4.0, 4.0],
			[1.0, 1.0]
		]
		self.B = [
			[9.0, 9.0],
			[3.0, 3.0],
			[2.0, 2.0],
			[4.0, 3.0],
			[1.0, 1.0]
		]	


	def testLen(self):
		A, B, genes = avg_dups(self.A, self.B, self.genes)
		self.assertEqual(len(A), 3)
		self.assertEqual(len(A), len(B))
		self.assertEqual(len(A), len(genes))


	def testData(self):
		genes_ans = ['A', 'B', 'C']
		A_ans = [
			[1.5, 1.5],
			[4.0, 4.0],
			[5.5, 5.5]
		]
		B_ans = [
			[5.0, 5.0],
			[4.0, 3.0],
			[2.5, 2.5]
		]

		A, B, genes = avg_dups(self.A, self.B, self.genes)
		self.assertTrue(np.array_equal(A, A_ans))
		self.assertTrue(np.array_equal(B, B_ans))
