"""POSTs data to crowdsourcing project:
http://www.maayanlab.net/crowdsourcing/
https://www.coursera.org/course/bd2klincs

__authors__ = "Gregory Gundersen, Zichen Wang"
__contact__ = "avi.maayan@mssm.edu"
"""


import requests


CROWDSOURCING_URL = 'http://maayanlab.net/crowdsourcing/g2e.php'

CROWDSOURCING_TAGS = {
    'AGING_BD2K_LINCS_DCIC_COURSERA': ['young', 'old', 'age_unit'],
    'MCF7_BD2K_LINCS_DCIC_COURSERA': ['pert_type', 'pert_name', 'pert_id'],
    'DISEASES_BD2K_LINCS_DCIC_COURSERA': ['disease_name', 'disease_id'],
    'LIGANDS_BD2K_LINCS_DCIC_COURSERA': ['ligand_name', 'ligand_id'],
    'DRUGS_BD2K_LINCS_DCIC_COURSERA': ['drug_name', 'drug_id'],
    'GENES_BD2K_LINCS_DCIC_COURSERA': ['pert_type'],
    'PATHOGENS_BD2K_LINCS_DCIC_COURSERA': ['microbe_name', 'microbe_id']
}


def post_if_necessary(genes, required_metadata, optional_metadata, soft_file, tags):
    for tag in tags:
        if tag.name in CROWDSOURCING_TAGS:
            __post(genes, required_metadata, optional_metadata, soft_file, tag)


def __post(genes, required_metadata, optional_metadata, soft_file, tag):

    payload = {
        'hashtag': tag.name,
        'geo_id': soft_file.platform,
        'ctrl_ids': [x.name for x in soft_file.samples if x.is_control],
        'pert_ids': [x.name for x in soft_file.samples if not x.is_control],
        'gene': __get_metadata_value_by_name(optional_metadata, 'gene'),
        'cell_type': __get_metadata_value_by_name(optional_metadata, 'cell'),
        'organism': __get_metadata_value_by_name(optional_metadata, 'organism'),
        'up_genes': [x.gene.name for x in genes if x.value > 0],
        'dn_genes': [x.gene.name for x in genes if x.value < 0],
        'email': 'g.gundersen@gmail.com',
        'key': 'b24f593f1779504260fe8318d243285f'
    }

    import pdb; pdb.set_trace()

    # microtask-specifc keys
    for field in CROWDSOURCING_TAGS[tag.name]:
        payload[field] = __get_metadata_value_by_name(
            optional_metadata, field
        )

    r = requests.post(CROWDSOURCING_URL, data=payload)

    print 'CROWDSOURCING:'
    print r.text
    print r.status_code
    print r.headers


def __get_metadata_value_by_name(optional_metadata, name):
    for opt_meta in optional_metadata:
        if opt_meta.name == name:
            return opt_meta.value