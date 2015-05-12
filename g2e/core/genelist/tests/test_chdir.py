import unittest
import numpy as np

from g2e.core.genelist.chdir import chdir
from g2e.core.genelist.chdir import _sort_by_coefficients


class TestChdir(unittest.TestCase):


    def setUp(self):
        # Get ordered list of values.
        answers = []
        with open('g2e/core/genelist/tests/data/chdir_output.txt', 'r') as out:
            for line in out:
                answers.append(float(line))
        self.answers = np.array(answers)

        genes = []
        A = []
        B = []
        with open('g2e/core/genelist/tests/data/example_input.txt', 'r') as inp:
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


    def testSumSquares(self):
        s = np.sum(np.square(self.values))
        close_enough = np.isclose(1,s)
        self.assertTrue(close_enough)


    def testChdir(self):
        delta = (self.answers - self.values) / self.answers
        close_enough = np.any(np.absolute(delta) < 0.0025)
        self.assertTrue(close_enough)


    def test_sort(self):
        genes, values = _sort_by_coefficients(
            ['A', 'B', 'C', 'D', 'E', 'F'],
            [0.4, 0.6, -0.44, -0.1, 0.2, 0.3]
        )
        self.assertEqual(genes, ['D', 'E', 'F', 'A', 'C', 'B'])
        self.assertEqual(values, [-0.1, 0.2, 0.3, 0.4, -0.44, 0.6])
