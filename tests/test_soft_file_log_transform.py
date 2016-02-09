import unittest
import numpy as np

from g2e.signaturefactory.softfileutils.cleaner import log2, _is_log


class TestLog2(unittest.TestCase):

    def test_log2(self):
        in_ = [[1.0, 2000.0, 17.3, 60.0],
               [.333, 3.141, 139.0, .5]]
        ans = [[0.0, 10.96578428, 4.11270013, 5.9068906],
               [-1.58640592, 1.65122394, 7.11894107, -1.0]]
        vals = log2(in_)
        self.assertTrue(np.allclose(vals, ans))

    def test_is_log2(self):
        self.assertTrue(_is_log([[1, 3], [2, 4]]))
        self.assertFalse(_is_log([[1, 3], [2, 102]]))
