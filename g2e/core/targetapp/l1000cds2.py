"""Handles L1000CDS2's API.
See http://amp.pharm.mssm.edu/L1000CDS2/
"""


import json
import requests


L1000CDS2_URL = 'http://amp.pharm.mssm.edu/L1000CDS2/'


def get_link(genes, metadata):
    """Returns a shareable link to L1000CDS2 data.
    """
    print 'Calculating cosine distance'

    url = L1000CDS2_URL + 'query'
    headers = { 'content-type': 'application/json' }
    payload = {
        'data': {
            'genes': [rg.gene.name for rg in genes],
            'vals': [float('{0:.6f}'.format(rg.value)) for rg in genes]
        },
        'config': {
            'aggravate': False,
            'searchMethod': 'CD',
            'share': False,
            'combination': False,
            'db-version': 'latest'
        },
        'metadata': metadata.to_L1000CDS2_data_format()
    }
    sess = requests.session()
    resp = sess.post(url, data=json.dumps(payload), headers=headers)

    if resp.status_code == 200:
        share_id = json.loads(resp.text)['shareId']
        link = L1000CDS2_URL + '#/result/' + share_id
        print 'Link to L100CDS2: ' + link
        return link
    else:
        print 'Error with L1000CDS2'
        return None
