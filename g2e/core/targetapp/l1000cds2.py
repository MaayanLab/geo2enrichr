"""Handles L1000CDS2's API. For more information, see:
http://amp.pharm.mssm.edu/L1000CDS2/help/

__authors__ = "Gregory Gundersen, Qiaonan Duan"
__contact__ = "avi.maayan@mssm.edu"
"""


import json
import requests


BASE_URL = 'http://amp.pharm.mssm.edu/L1000CDS2/'


def get_link(genes, metadata):
    """Returns a shareable link to L1000CDS2 data.
    """
    print 'Calculating cosine distance'

    genes, values = zip(*genes)
    url = BASE_URL + 'query'
    headers = { 'content-type': 'application/json' }
    payload = {
        'data': {
            'genes': genes,
            'vals': [float('{0:.6f}'.format(x)) for x in values]
        },
        'config': {
            'aggravate': False,
            'searchMethod': 'CD',
            'share': False,
            'combination': False
        },
        'metadata': metadata.to_L1000CDS2_data_format()
    }
    sess = requests.session()
    resp = sess.post(url, data=json.dumps(payload), headers=headers)

    if resp.status_code == 200:
        share_id = json.loads(resp.text)['shareId']
        link = BASE_URL + '#/result/' + share_id
        print 'Link to L100CDS2: ' + link
        return link
    else:
        print 'Error with L1000CDS2'
        return None
