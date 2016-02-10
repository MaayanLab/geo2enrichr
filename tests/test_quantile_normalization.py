import unittest
import numpy as np

from g2e.signature_factory.soft_file_factory.cleaner import quantile_normalization


class TestQuantileNormalization(unittest.TestCase):

    def setUp(self):
        self.vals = np.array(
            [[1.0, 2.0, 3.0, 5.0],
             [9.0, 14.0, 42.0, 14.0],
             [3.0, 1.0, 7.0, 4.0],
             [7.0, 20.0, 1.0, 1.0],
             [3.0, 79.0, 16.0, 11.0]])

    def test_quantile_normalization(self):
        ans = np.array(
            [[1.0, 3.0, 3.0, 7.25],
             [36.0, 7.25, 36.0, 36.0],
             [3.0, 1.0, 7.25, 3.0],
             [13.5, 13.5, 1.0, 1.0],
             [7.25, 36, 13.5, 13.5]])

        vals = quantile_normalization(self.vals)
        self.assertTrue(np.array_equal(vals, ans))

    def test_quantile_normalization_on_normalized_data(self):
        vals = quantile_normalization(self.vals)
        # ans is the qnorm of normalized data; this should be the same as the
        # input.
        ans = quantile_normalization(vals)
        self.assertTrue(np.array_equal(vals, ans))
