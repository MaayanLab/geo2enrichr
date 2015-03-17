import json
import unittest

import app


unittest.TestCase.maxDiff = None


def get_gene_value(genelist, gene):
    for gv in genelist['ranked_genes']:
        if gv[0] == gene:
            return gv[1]
    return None


class ExtractEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.resp = self.app.post('/g2e/extract', data=dict(
            is_geo = 'True',
            dataset = 'GDS5077',
            platform = 'GPL10558',
            A_cols = ['GSM1071454', 'GSM1071455'],
            B_cols = ['GSM1071457', 'GSM1071456']
        ))
        self.resp_dict = json.loads(self.resp.data.decode())

    # This should be multiple unit tests but it is annoyingly slow to run.
    def test_extraction_endpoint(self):
        self.assertEquals(self.resp.status_code, 200)
        self.assertTrue('extraction_id' in self.resp_dict)

        extraction_id = self.resp_dict['extraction_id']
        resp = self.app.get('/g2e/extract?id=' + str(extraction_id))
        resp_dict = json.loads(resp.data.decode())

        self.assertTrue(resp_dict['method'] == 'chdir')
        self.assertTrue(resp_dict['cutoff'] == 500)
        self.assertTrue(resp_dict['softfile']['name'] == 'GDS5077')
        self.assertTrue('enrichr_link_up' in resp_dict)
        self.assertTrue('enrichr_link_down' in resp_dict)
        self.assertTrue('text_file' in resp_dict['softfile'])
        self.assertTrue('genelist' in resp_dict)

        genelist = resp_dict['genelist']
        self.assertTrue(get_gene_value(genelist, 'HBE1') == -0.0886708)
        self.assertTrue(get_gene_value(genelist, 'EOMES') == 0.0868757)
        self.assertTrue(get_gene_value(genelist, 'SRPK1') == -0.0215827)
        self.assertTrue(get_gene_value(genelist, 'MYH6') == -0.030176)
