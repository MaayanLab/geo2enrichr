import unittest
import numpy as np

from g2e.cleaner import log2, _is_log2


class TestLog2(unittest.TestCase):


	def testLog2(self):
		A_in = [[1.0,   2000.0],
			    [.333,  3.141]]
		B_in = [[17.3,  60.0],
			    [139.0, .5]]

		A_ans = [[0.0,         10.96578428],
			     [-1.58640592, 1.65122394]]
		B_ans = [[4.11270013,  5.9068906],
			     [7.11894107,  -1.0]]

		A, B = log2(A_in, B_in)
		self.assertTrue(np.allclose(A, A_ans))
		self.assertTrue(np.allclose(B, B_ans))


	def testIsLog2(self):
		# AB = np.concatenate((A, B), axis=1)
		# AB_max = np.amax(AB)
		# AB_min = np.amin(AB)
		# if AB_max - AB_min < 100:
		#	return True
		# return False
		pass