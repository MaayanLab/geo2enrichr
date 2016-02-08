import unittest

import numpy as np
from g2e.diffexp.analysis import _throw_away_rows_without_variance


class TestThrowAwayRowsWithoutVarianece(unittest.TestCase):

    def test_all_zeros(self):
        A = np.array([
            [1,2],
            [3,5],
            [0,0],
            [0,0]
        ])
        B = np.array([
            [3,1],
            [2,2],
            [0,0],
            [0,1]
        ])
        genes = np.array(['A','B','C','D'])
        A, B, genes = _throw_away_rows_without_variance(A, B, genes)
        self.assertTrue('C' not in genes)
        self.assertTrue(len(genes) is 3)
        self.assertTrue(np.array_equal(A[2], [0,0]))
        self.assertTrue(np.array_equal(B[2], [0,1]))

    def test_all_constants(self):
        A = np.array([
            [20,20],
            [5,0]
        ])
        B = np.array([
            [20,20],
            [0,1]
        ])
        genes = np.array(['A','B'])
        A, B, genes = _throw_away_rows_without_variance(A, B, genes)
        self.assertTrue('A' not in genes)
        self.assertTrue(len(genes) is 1)
        self.assertTrue(np.array_equal(A[0], [5,0]))
        self.assertTrue(np.array_equal(B[0], [0,1]))

