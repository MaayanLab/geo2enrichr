import unittest

from flask import request
from g2e import app
from g2e.endpoints.requestutil import get_param_as_list


class TestRequestUtil(unittest.TestCase):

    def setUp(self):
        # We just want to create and test against a real request object,
        # particularly with the `getlist` function.
        self.app = app.test_client()

    def testWithCommas(self):
        with app.test_request_context('/fake_endpoint?p=foo,bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')

    def testWithDuplicates(self):
        with app.test_request_context('/fake_endpoint?p=foo&p=bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')

    def testWithBrackets(self):
        with app.test_request_context('/fake_endpoint?p[]=foo&p[]=bar', method='GET'):
            x = get_param_as_list(request.args, 'p')
            self.assertTrue(len(x), 2)
            self.assertTrue(x[0], 'foo')
            self.assertTrue(x[1], 'bar')