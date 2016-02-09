import unittest

from substrate import SoftFileSample

import g2e.signaturefactory.softfileutils.parser as softparser


class TestSoftFileParser(unittest.TestCase):

    def test_geo_soft_file_parser(self):
        samples = [
            SoftFileSample('GSM1071455', True),
            SoftFileSample('GSM1071454', True),
            SoftFileSample('GSM1071457', False),
            SoftFileSample('GSM1071456', False)
        ]

        genes, a_vals, b_vals, selections, stats = softparser._parse_geo(
            'tests/data/GDS5077.txt', 'GPL10558', samples
        )

        self.assertEqual(len(genes), 31115)
        self.assertEqual(len(a_vals), 31115)
        self.assertEqual(len(b_vals), 31115)
        self.assertEqual(selections['a_indices'], [3, 2])
        self.assertEqual(selections['b_indices'], [0, 1])
        self.assertEqual(stats['discarded_lines_pct'], 0.0021131373750607526)
        self.assertEqual(stats['unconverted_probes_pct'], 34.248341152106846)

    def test_custom_soft_file_parser(self):
        genes, a_vals, b_vals, samples = softparser._parse_file(
            'tests/data/example_input.txt'
        )

        self.assertEqual(len(genes), 978)
        self.assertEqual(len(a_vals), 978)
        self.assertEqual(len(b_vals), 978)

        # These genes are randomly selected. A passing test does *not* mean
        # the parser is fine. But it should provide some sanity checking.
        for symbol in ['PSME1', 'POLG2', 'ATG3', 'WDTC1', 'LSM6', 'PTPRC', 'FBXO21', 'PTPN12', 'LYRM1']:
            self.assertTrue(symbol in genes)

        # Just checking the edge cases.
        self.assertEqual(a_vals[0][0], 11.0434)
        self.assertEqual(a_vals[38][19], 8.0992)
        self.assertEqual(b_vals[977][5], 4.7527)