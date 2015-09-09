import json
import unittest

from g2e import app


class TestTargetApps(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_target_apps_chdir(self):
        post_response = self.app.post('/g2e/api/extract/geo', data=dict(
            dataset = 'GDS5077',
            platform = 'GPL10558',
            organism = 'Homo sapiens',
            A_cols = ['GSM1071454', 'GSM1071455'],
            B_cols = ['GSM1071457', 'GSM1071456']
        ))
        post_response = json.loads(post_response.data.decode())
        extraction_id = post_response['extraction_id']
        response = self.app.get('/g2e/api/extract/' + str(extraction_id))
        response = json.loads(response.data.decode())

        for gl in response['gene_lists']:
            self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in gl['target_apps']['enrichr'])
            if gl['direction'] == 0:
                self.assertTrue('http://amp.pharm.mssm.edu/L1000CDS2' in gl['target_apps']['l1000cds2'])
                self.assertTrue('http://amp.pharm.mssm.edu/PAEA' in gl['target_apps']['paea'])
            else:
                raised1 = False
                try:
                    gl['target_apps']['paea']
                except KeyError:
                    raised1 = True
                self.assertTrue(raised1)

                raised2 = False
                try:
                    gl['target_apps']['l1000cds2']
                except KeyError:
                    raised2 = True
                self.assertTrue(raised2)