"""Handles Enrichr's API.

__authors__ = "Gregory Gundersen, Qiaonan Duan"
__contact__ = "avi.maayan@mssm.edu"
"""


import json
import time
import requests


BASE_URL = 'http://amp.pharm.mssm.edu/Enrichr/'


def get_link(genes, description):
    """Returns a shareable link to Enrichr.
    """
    # Enrichr does not care about the sign of the rank; it treats the rank
    # simply as a membership value for a fuzzy set.
    genes = [(t[0], str(abs(t[1]))) for t in genes]

    genes_str = '\n'.join([t[0] + ',' + t[1] for t in genes]).encode('ascii')
    payload = {
        'list': genes_str,
        'description': description
    }
    sess = requests.session()

    # 1. POST the data to the server. We do not need the response.
    sess.post(BASE_URL + 'enrich', files={ 'list': (None, genes_str), 'description': (None, description) })

    # I've noticed that sometimes the GET errors out and wonder if it is a
    # race condition of some sort. This throttles the back-to-back requests
    # and seems to resolve the issue on our end.
    time.sleep(0.5)

    # 2. GET our link via the "share" endpoint. The requests module (and
    # Enrichr handle cookies for us.
    resp = sess.get(BASE_URL + 'share')
    if resp.status_code == 200:
        link_id = json.loads(resp.text)['link_id']
        print 'Link to enrichr: ' + link_id
        return BASE_URL + 'enrich?dataset=' + link_id
    else:
        print 'Error with Enrichr'
        return None
