import unittest

from flask import request
from g2e import app
from g2e.endpoints.request_utils import get_param_as_list


class TestRequestUtils(unittest.TestCase):

    def setUp(self):
        # We just want to create and test against a real request object,
        # particularly with the `getlist` function.
        self.app = app.test_client()

    def test_with_commas(self):
        with app.test_request_context('/fake_endpoint?p=foo,bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')

    def test_with_duplicates(self):
        with app.test_request_context('/fake_endpoint?p=foo&p=bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')

    def test_with_brackets(self):
        with app.test_request_context('/fake_endpoint?p[]=foo&p[]=bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')