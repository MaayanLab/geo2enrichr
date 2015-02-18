import json
import unittest

from tests.util import toJSON
import app


class DlGeoEndpoint(unittest.TestCase):


    def setUp(self):
        self.app = app.app.test_client()


    def test_full_endpoint(self):
    	headers = [('Content-Type', 'application/json')]
    	data = json.dumps({
			'accession': 'GSE62359',
			'platform': 'GPL10558'
    	})
        resp = toJSON(self.app.put('/g2e/dlgeo', data=data, headers=headers))
        correct_resp = toJSON('dlgeo_response.txt')
        self.assertEqual(resp, correct_resp)
