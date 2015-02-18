import unittest

from tests.util import toJSON
import app


unittest.TestCase.maxDiff = None


class FullEndpoint(unittest.TestCase):


    def setUp(self):
        self.app = app.app.test_client()


    def test_index(self):
        resp = toJSON(self.app.get('/g2e'))
        correct_resp = toJSON('index_response.txt')
        self.assertEqual(resp, correct_resp)
