import json
import unittest

from g2e import app


class TestClusterEndpoint(unittest.TestCase):

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
        post_response = json.loads(temp.data.decode('utf-8'))
        self.extraction_id = post_response['extraction_id']

    def test_endpoint(self):
        url = '/g2e/cluster/' + self.extraction_id
        response = self.app.get(url)
        self.assertTrue('https://amp.pharm.mssm.edu/clustergrammer/viz/' in response.data)
