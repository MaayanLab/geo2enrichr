"""Handles Enrichr's API.
See http://amp.pharm.mssm.edu/Enrichr/
"""


import json
import time
import requests


ENRICHR_URL = 'https://amp.pharm.mssm.edu/Enrichr/'


def get_link(ranked_genes, description):
    """Returns a shareable link to Enrichr.
    """
    genes = convert_ranked_genes_to_tuples(ranked_genes)
    genes_str = get_genes_as_string(genes)

    sess = requests.session()

    # 1. POST the data to the server. We do not need the response.
    sess.post(ENRICHR_URL + 'enrich', files={ 'list': (None, genes_str), 'description': (None, description) })

    # I've noticed that sometimes the GET errors out and wonder if it is a
    # race condition of some sort. This throttles the back-to-back requests
    # and seems to resolve the issue on our end.
    time.sleep(1)

    # 2. GET our link via the "share" endpoint. The requests module (and
    # Enrichr handle cookies for us.
    resp = sess.get(ENRICHR_URL + 'share')
    if resp.status_code == 200:
        link_id = json.loads(resp.text)['link_id']
        print('Link to enrichr: ' + link_id)
        return ENRICHR_URL + 'enrich?dataset=' + link_id
    else:
        print('Error with Enrichr')
        return None


def convert_ranked_genes_to_tuples(ranked_genes):
    """Converts RankedGene instances to tuples appropriate for Enrichr.
    """
    # Enrichr does not care about the sign of the rank; it treats the rank
    # simply as a membership value for a fuzzy set.
    return [(rg.gene.name, str(abs(rg.value))) for rg in ranked_genes]


def get_genes_as_string(genes):
    """Returns string from list of gene tuples.
    """
    return '\n'.join([t[0] + ',' + t[1] for t in genes])