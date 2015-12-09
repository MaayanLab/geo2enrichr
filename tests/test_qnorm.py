import unittest
import numpy as np

from g2e.core.softutils.cleaner import qnorm


class TestQnorm(unittest.TestCase):

    def setUp(self):
        self.vals = np.array(
            [[1.0, 2.0, 3.0, 5.0],
             [9.0, 14.0, 42.0, 14.0],
             [3.0, 1.0, 7.0, 4.0],
             [7.0, 20.0, 1.0, 1.0],
             [3.0, 79.0, 16.0, 11.0]])

    def testQnorm(self):
        ans = np.array(
            [[1.0, 3.0, 3.0, 7.25],
             [36.0, 7.25, 36.0, 36.0],
             [3.0, 1.0, 7.25, 3.0],
             [13.5, 13.5, 1.0, 1.0],
             [7.25, 36, 13.5, 13.5]])

        vals = qnorm(self.vals)
        self.assertTrue(np.array_equal(vals, ans))

    def testQnormOnNormalizedData(self):
        vals = qnorm(self.vals)
        # ans is the qnorm of normalized data; this should be the same as the
        # input.
        ans = qnorm(vals)
        self.assertTrue(np.array_equal(vals, ans))
