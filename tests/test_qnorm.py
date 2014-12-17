import unittest
import numpy as np

from g2e.cleaner import qnorm


class TestQnorm(unittest.TestCase):


	def setUp(self):
		self.A = [
			[1.0, 2.0],
			[9.0, 14.0],
			[3.0, 1.0],
			[7.0, 20.0],
			[3.0, 79.0]
		]
		self.B = [
			[3.0, 5.0],
			[42.0, 14.0],
			[7.0, 4.0],
			[1.0, 1.0],
			[16.0, 11.0]
		]


	def testQnorm(self):
		A_ans = np.array([
			[1.0, 3.0],
			[36.0, 7.25],
			[3.0, 1.0],
			[13.5, 13.5],
			[7.25, 36]
		])
		B_ans = np.array([
			[3.0, 7.25],
			[36.0, 36.0],
			[7.25, 3.0],
			[1.0, 1.0],
			[13.5, 13.5],
		])

		A, B = qnorm(self.A, self.B)
		self.assertTrue(np.array_equal(A, A_ans))
		self.assertTrue(np.array_equal(B, B_ans))


	def testQnormOnNormalizedData(self):
		A_ans = np.array([
			[1.0, 3.0],
			[36.0, 7.25],
			[3.0, 1.0],
			[13.5, 13.5],
			[7.25, 36]
		])
		B_ans = np.array([
			[3.0, 7.25],
			[36.0, 36.0],
			[7.25, 3.0],
			[1.0, 1.0],
			[13.5, 13.5],
		])

		A, B = qnorm(self.A, self.B)
		A, B = qnorm(A, B)
		self.assertTrue(np.array_equal(A, A_ans))
		self.assertTrue(np.array_equal(B, B_ans))