import unittest
import numpy as np

from dataprocessor.cleaner import _remove_negatives


class TestRemoveNegatives(unittest.TestCase):


	def setUp(self):
		self.genes = ['A', 'C', 'C', 'B', 'A']
		self.A = [
			[2.0, 2.0],
			[-3.0, 3.0],
			[8.0, 8.0],
			[4.0, 4.0],
			[1.0, 1.0]
		]
		self.B = [
			[9.0, 9.0],
			[3.0, 3.0],
			[2.0, -2.0],
			[4.0, 3.0],
			[1.0, 1.0]
		]


	def testNegs(self):
		A, B, genes = _remove_negatives(self.A, self.B, self.genes)
		# AB[1] and AB[2] should have been removed because they contain
		# negative numbers.
		ansA = np.array([[2.0,2.0],[4.0,4.0],[1.0,1.0]])
		self.assertTrue((A == ansA).all())
		ansB = np.array([[9.0,9.0],[4.0,3.0],[1.0,1.0]])
		self.assertTrue((B == ansB).all())


	def testLens(self):
		A, B, genes = _remove_negatives(self.A, self.B, self.genes)
		self.assertEqual(len(A), 3)
		self.assertEqual(len(A), len(B))
		self.assertEqual(len(A), len(genes))
