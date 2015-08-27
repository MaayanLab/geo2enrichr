"""POSTs data to crowdsourcing project:
http://www.maayanlab.net/crowdsourcing/
https://www.coursera.org/course/bd2klincs

__authors__ = "Gregory Gundersen, Zichen Wang"
__contact__ = "avi.maayan@mssm.edu"
"""


import requests


CROWDSOURCING_URL = 'http://maayanlab.net/crowdsourcing/g2e.php'

CROWDSOURCING_TAGS = [
    'AGING_BD2K_LINCS_DCIC_COURSERA',
    'MCF7_BD2K_LINCS_DCIC_COURSERA',
    'DISEASES_BD2K_LINCS_DCIC_COURSERA',
    'LIGANDS_BD2K_LINCS_DCIC_COURSERA',
    'DRUGS_BD2K_LINCS_DCIC_COURSERA',
    'GENES_BD2K_LINCS_DCIC_COURSERA',
    'PATHOGENS_BD2K_LINCS_DCIC_COURSERA'
]


def post_if_necessary(genes, metadata, tags):
    for tag in tags:
        if tag in CROWDSOURCING_TAGS:
            __post(genes, metadata, tag)


def __post(genes, metadata, tag):
    pass
    #
    # payload = {
    #     ## required keys
    #     'geo_id': 'GSEtest3',
    #     'ctrl_ids': 'GSMtest1,GSMtest00',
    #     'pert_ids': 'GSMtest3,GSMtest4',
    #     'gene': 'testGene',
    #     'cell_type': 'MCF7',
    #     'organism': 'human',
    #     'up_genes': 'any text here',
    #     'dn_genes': 'any text here',
    #     'email': 'wangzc921@gmail.com',
    #     'key': '4e7d397e8d2badbdde1eefec33b8a591',
    #
    #     ## hashtag
    #     'hashtag': '#MCF7_BD2K_LINCS_DCIC_COURSERA',
    #
    #     ## microtask-specifc keys
    #     'pert_type': 'KO',
    #     }
    #
    # r = requests.post(CROWDSOURCING_URL, data=payload)
    #
    # print r.text
    # print r.status_code
    # print r.headers
