import unittest
import numpy as np

from core.genelist.chdir import chdir


class TestChdir(unittest.TestCase):


	def setUp(self):
		# Get ordered list of values.
		answers = []
		with open('core/softfile/tests/data/chdir_output.tsv', 'r') as out:
			for line in out:
				answers.append(float(line))
		self.answers = np.array(answers)

		genes = []
		A = []
		B = []
		with open('core/softfile/tests/data/chdir_input.txt', 'r') as inp:
			discard = next(inp)
			header = next(inp)
			for line in inp:
				split = line.split('\t')
				genes.append(split[0])
				A_row = split[1:21]
				B_row = split[21:]
				A.append([float(pv) for pv in A_row])
				B.append([float(pv) for pv in B_row])

		self.genes, self.values = chdir(A, B, genes)


	def testRootSumSquares(self):
		RMS = np.sqrt(np.sum( np.square( self.values ) ))
		delta = abs(RMS - 1.0)
		self.assertTrue(delta < 0.00000001)


	def testChdir(self):
		in_range = abs(self.answers - self.values < 0.01)
		self.assertTrue(np.any(in_range))
