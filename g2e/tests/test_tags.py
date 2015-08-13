import json
import unittest

from g2e import app


class ExtractEndpoint(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()


    def test_tags(self):
        print 'Testing tags'
        self.resp = self.app.post('/g2e/api/extract/upload', data=dict(
            file = (file('g2e/core/genelist/tests/data/example_input.txt'), 'test.txt'),
            diffexp_method = 'ttest',
            name = 'ExampleData',
            cutoff = 'none',
            tags = json.dumps(['food', 'cats', 'beer']),
            skip_target_apps = True
        ))
        extraction_id = json.loads(self.resp.data.decode())['extraction_id']
        resp = self.app.get('/g2e/api/extract/' + str(extraction_id))
        response = json.loads(resp.data.decode())
        tags = response['tags']
        self.assertTrue(len(tags) == 3)
        self.assertTrue('food' in tags)
        self.assertTrue('cats' in tags)
        self.assertTrue('beer' in tags)