import json
import unittest

from tests.util import toJSON
import app


unittest.TestCase.maxDiff = None


class DiffExpEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_diffexp_endpoint(self):
    	headers = [('Content-Type', 'application/json')]
    	data = toJSON('diffexp_request.txt')
    	resp = toJSON(self.app.post('/g2e/diffexp', data=data, headers=headers))
        print resp
        #correct_resp = toJSON('getgeo_response.txt')
        #self.assertEqual(resp, correct_resp)
