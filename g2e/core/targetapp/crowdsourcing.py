"""POSTs data to crowdsourcing project:
http://www.maayanlab.net/crowdsourcing/
https://www.coursera.org/course/bd2klincs

__authors__ = "Gregory Gundersen, Zichen Wang"
__contact__ = "avi.maayan@mssm.edu"
"""


import json
import time

import requests

from g2e.config import Config


CROWDSOURCING_POST_URL = 'http://maayanlab.net/crowdsourcing/g2e.php'
CROWDSOURCING_LEADERBOARD_BASE_URL = 'http://maayanlab.net/crowdsourcing/microtask_leaderboard.php'

CROWDSOURCING_TAGS = {
    'AGING_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['young', 'old', 'age_unit'],
        'task_num': 5
    },
    'MCF7_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['pert_type', 'pert_name', 'pert_id'],
        'task_num': 4
    },
    'DISEASES_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['disease_name', 'disease_id'],
        'task_num': 2
    },
    'LIGANDS_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['ligand_name', 'ligand_id'],
        'task_num': 6
    },
    'DRUGS_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['drug_name', 'drug_id'],
        'task_num': 3
    },
    'GENES_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['pert_type'],
        'task_num': 1
    },
    'PATHOGENS_BD2K_LINCS_DCIC_COURSERA': {
        'fields': ['microbe_name', 'microbe_id'],
        'task_num': 7
    }
}


def post_if_necessary(genes, optional_metadata, soft_file, tags):
    print 'POSTing to Crowdsourcing if necessary'

    tags_to_post = []
    for tag in tags:
        if tag.name in CROWDSOURCING_TAGS:
            tags_to_post.append(tag)

    results = {}
    for tag in tags_to_post:
        response = _post(genes, optional_metadata, soft_file, tag)
        if response['status_code'] == 200:
            link = CROWDSOURCING_LEADERBOARD_BASE_URL + '#task' + str(CROWDSOURCING_TAGS[tag.name]['task_num'])
            results[tag.name] = link
        else:
            # If multiple errors occur, this only saves the last one but
            # that's fine.
            results['message'] = response['message']

    return results


def _post(genes, optional_metadata, soft_file, tag):
    print '\tPOSTing ' + tag.name

    # If we submit an identical study (same GDS or GSE with the same GSMs),
    # the crowdsourcing app rejects the study. For testing purposes, we want
    # to verify that the endpoint works. So we just generate a random string
    # for the control GSMs.
    if Config.DEBUG:
        ctrl_ids = str(time.time())
    else:
        ctrl_ids = ','.join([x.name for x in soft_file.samples if x.is_control])

    payload = {
        'hashtag': '#' + tag.name,
        'geo_id': soft_file.platform,
        'ctrl_ids': ctrl_ids,
        'pert_ids': ','.join([x.name for x in soft_file.samples if not x.is_control]),
        'gene': _get_metadata_value_by_name(optional_metadata, 'gene'),
        'cell_type': _get_metadata_value_by_name(optional_metadata, 'cell'),
        'organism': _get_metadata_value_by_name(optional_metadata, 'organism'),
        'up_genes': ','.join([x.gene.name for x in genes if x.value > 0]),
        'dn_genes': ','.join([x.gene.name for x in genes if x.value < 0]),

        # TODO: Read these in from the extension.
        'email': _get_metadata_value_by_name(optional_metadata, 'user_email'),
        'key': _get_metadata_value_by_name(optional_metadata, 'user_key')
    }

    # microtask-specifc keys
    for field in CROWDSOURCING_TAGS[tag.name]['fields']:
        payload[field] = _get_metadata_value_by_name(
            optional_metadata, field
        )

    response = requests.post(CROWDSOURCING_POST_URL, data=payload)
    return {
        'status_code': response.status_code,
        'message': json.loads(response.text)['message']
    }


def _get_metadata_value_by_name(optional_metadata, name):
    for opt_meta in optional_metadata:
        if opt_meta.name == name:
            return opt_meta.value
    return ''
