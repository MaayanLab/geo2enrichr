import json
import unittest

from g2e import app


class TestCluster(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        temp = self.app.post('/g2e/api/extract/geo', data=dict(
            skip_target_apps=True,
            is_geo=True,
            # T-test is just faster
            diffexp_method='ttest',
            correction_metrequired_metadatahod='BH',
            threshold=0.05,
            dataset='GDS5077',
            platform='GPL10558',
            organism='Homo sapiens',
            normalize=False,
            A_cols=['GSM1071454', 'GSM1071455'],
            B_cols=['GSM1071457', 'GSM1071456']
        ))
        post_response = json.loads(temp.data.decode())
        self.extraction_id = post_response['extraction_id']
        temp = self.app.get('/g2e/api/extract/' + str(self.extraction_id))
        response = json.loads(temp.data.decode())

        self.direction = 0
        self.up_gene_list = response['gene_lists'][self.direction]

    def testEndpoint(self):
        print(self.extraction_id)
        url = '/g2e/cluster/' + self.extraction_id
        response = self.app.get(url)
        self.assertTrue('http://amp.pharm.mssm.edu/clustergrammer/viz/' in response.data)
