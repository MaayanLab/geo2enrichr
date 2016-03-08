"""Functions for fetching data from GEO's EUtils API.
"""

import json

import requests


BASE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/{0}.fcgi?db=gds&retmax=1&retmode=json'


def get_title_and_summary(accession):
    """Returns title and summary based on accession.
    """
    if 'GDS' in accession:
        search_url = BASE_URL.replace('{0}', 'esearch') + '&term=' + accession
        resp = requests.get(search_url)
        data = json.loads(resp.text)
        accession_id = data['esearchresult']['idlist'][0]
    else:
        accession_id = accession[3:]

    summary_url = BASE_URL.replace('{0}', 'esummary') + '&id=' + accession_id
    resp = requests.get(summary_url)
    data = json.loads(resp.text)
    data = data.get('result').get(accession_id)

    if data.get('error') == 'cannot get document summary':
        return None, None

    return data.get('title'), data.get('summary')
