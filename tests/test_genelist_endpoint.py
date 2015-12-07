import unittest
import json
import csv
import StringIO

from g2e import app


class TestGeneListEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        temp = self.app.post('/g2e/api/extract/geo', data=dict(
            skip_target_apps = True,
            is_geo = True,
            # T-test is just faster
            diffexp_method = 'ttest',
            correction_metrequired_metadatahod = 'BH',
            threshold = 0.05,
            dataset = 'GDS5077',
            platform = 'GPL10558',
            organism = 'Homo sapiens',
            normalize = False,
            A_cols = ['GSM1071454', 'GSM1071455'],
            B_cols = ['GSM1071457', 'GSM1071456']
        ))
        post_response = json.loads(temp.data.decode())
        self.extraction_id = post_response['extraction_id']
        temp = self.app.get('/g2e/api/extract/' + str(self.extraction_id))
        response = json.loads(temp.data.decode())

        self.direction = 0
        self.up_gene_list = response['gene_lists'][self.direction]

    def testEndpoint(self):
        url = '/g2e/genelist/' + str(self.direction) + '/' + self.extraction_id
        response = self.app.get(url)
        self.assertEqual(response.mimetype, 'text/plain')

        f = StringIO.StringIO(response.data)
        reader = csv.reader(f, delimiter='\t')
        lines = [x for x in reader]

        self.assertEqual(lines[0], ['!direction', '0'])
        self.assertEqual(lines[1], ['!num_genes', '330'])
        self.assertEqual(lines[2], ['!diffexp_method', 'ttest'])
        self.assertEqual(lines[3], ['!cutoff', 'None'])
        self.assertEqual(lines[4], ['!correction_method', 'BH'])
        self.assertEqual(lines[5], ['!threshold', '0.05'])
        self.assertEqual(lines[6], ['!organism', 'Homo sapiens'])
        self.assertEqual(lines[7], ['!end_metadata'])
        self.assertEqual(len(lines), 338)
