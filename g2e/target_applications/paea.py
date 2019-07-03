"""Handles the Principle Angle Enrichment Analysis (PAEA) API.
See http://amp.pharm.mssm.edu/PAEA/
"""


import json
import requests


PAEA_POST_URL = 'https://amp.pharm.mssm.edu/Enrichr/addList'
PAEA_GET_URL  = 'https://amp.pharm.mssm.edu/PAEA?id='


def get_link(genes, description):
    """Returns a shareable link to PAEA data.
    """
    print('Calculating principle angle enrichment analysis')

    gene_list = ''
    for rg in genes:
        gene_list += '%s,%s\n' % (rg.gene.name, rg.value)
    
    payload = {
        'list': gene_list,
        'inputMethod': 'PAEA',
        'description': description
    }
    resp = requests.post(PAEA_POST_URL, files=payload)

    if resp.status_code == 200:
        link = PAEA_GET_URL + str(json.loads(resp.text)['userListId'])
        print('Link to PAEA: ' + link)
        return link
    else:
        print('Error with PAEA')
        return None
