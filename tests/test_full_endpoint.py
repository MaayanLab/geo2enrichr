import unittest

from tests.util import toJSON
import app


unittest.TestCase.maxDiff = None


class FullEndpoint(unittest.TestCase):


    def setUp(self):
        self.app = app.app.test_client()


    def test_full_endpoint(self):
        resp = toJSON(self.app.get('/g2e/full?accession=GDS5077&platform=GPL10558&control=GSM1071454-GSM1071455&experimental=GSM1071457-GSM1071456'))
        correct_resp = toJSON('full_response.txt')
        self.assertEqual(resp['up_genes'], correct_resp['up_genes'])
        self.assertEqual(resp['down_genes'], correct_resp['down_genes'])
       	self.assertEqual(resp['conversion_pct'], correct_resp['conversion_pct'])
