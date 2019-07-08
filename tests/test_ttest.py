import unittest

import numpy as np
from g2e.differential_expression.ttest import _get_pvalues


class TestTtest(unittest.TestCase):

    def setUp(self):
        # Get ordered list of values.
        answers = []
        with open('tests/data/ttest_output_corrected.txt', 'r', encoding='utf-8') as out:
            for line in out:
                ans = float(line.strip())
                answers.append(ans)
        self.answers = np.array(answers)

        genes = []
        A = []
        B = []
        with open('tests/data/example_input.txt', 'r', encoding='utf-8') as inp:
            discard = next(inp)
            header = next(inp)
            for line in inp:
                split = line.split('\t')
                genes.append(split[0])
                A_row = split[1:21]
                B_row = split[21:]
                A.append([float(pv) for pv in A_row])
                B.append([float(pv) for pv in B_row])

        genes, values = _get_pvalues(A, B, genes)
        self.genes = np.array(genes)
        self.values = np.array(values)

    def test_pvalue_answers(self):
        # Neil uses a one-tail t-test, while we use a two-tail t-test.
        # Hence, we scale by 2.
        delta = (self.answers - self.values / 2) / self.answers
        close_enough = np.any(np.absolute(delta) < 0.00001)
        self.assertTrue(close_enough)
