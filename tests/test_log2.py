import unittest
import numpy as np

from g2e.core.softfile.softcleaner import log2, _is_log


class TestLog2(unittest.TestCase):


	def testLog2(self):
		vals = [[1.0,  2000.0, 17.3,  60.0],
				[.333, 3.141, 139.0, .5]]
		ans  = [[0.0,         10.96578428, 4.11270013, 5.9068906],
			    [-1.58640592, 1.65122394, 7.11894107,  -1.0]]
		vals = log2(vals)
		self.assertTrue(np.allclose(vals, ans))


	def testIsLog2(self):
		self.assertTrue(_is_log([[1, 3], [2, 4]]))
		self.assertFalse(_is_log([[1, 3], [2, 102]]))
