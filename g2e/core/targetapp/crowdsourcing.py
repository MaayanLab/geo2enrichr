import requests


CROWDSOURCING_URL = 'http://maayanlab.net/crowdsourcing/g2e.php'


def get_link(genes, description):

    payload = {
        ## required keys
        'geo_id': 'GSEtest3',
        'ctrl_ids': 'GSMtest1,GSMtest00',
        'pert_ids': 'GSMtest3,GSMtest4',
        'gene': 'testGene',
        'cell_type': 'MCF7',
        'organism': 'human',
        'up_genes': 'any text here',
        'dn_genes': 'any text here',
        'email': 'wangzc921@gmail.com',
        'key': '4e7d397e8d2badbdde1eefec33b8a591',

        ## hashtag
        'hashtag': '#MCF7_BD2K_LINCS_DCIC_COURSERA',

        ## microtask-specifc keys
        'pert_type': 'KO',
        }

    r = requests.post(CROWDSOURCING_URL, data=payload)

    print r.text
    print r.status_code
    print r.headers
