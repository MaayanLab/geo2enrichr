import json
import unittest

from tests.util import toJSON
import app


unittest.TestCase.maxDiff = None


class GetGeoEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_full_endpoint(self):
    	headers = [('Content-Type', 'application/json')]
    	data = json.dumps({
			'dataset': 'GDS5077',
			'platform': 'GPL10558',
			'gsms': ['GSM1071454', 'GSM1071455', 'GSM1071457', 'GSM1071456']
    	})
        resp = toJSON(self.app.put('/g2e/getgeo', data=data, headers=headers))
        correct_resp = toJSON('getgeo_response.txt')
        self.assertEqual(resp, correct_resp)
