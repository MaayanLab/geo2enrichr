"""Handles all API endpoints to Enrichr.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, jsonify, request
import json
import requests

from g2e.dataaccess import dataaccess
from g2e.config import Config


enrichr_blueprint = Blueprint('enrichr', __name__, url_prefix=Config.BASE_URL + '/enrichr')


@enrichr_blueprint.route('', methods=['POST'])
def enrich_then_cluster_all_signatures():
    """Based on extraction IDs, post gene signatures to Enrichr and returns
    userListIds.
    """
    user_list_ids = []
    columns = {}
    for obj in request.json['signatures']:
        sig = dataaccess.fetch_gene_signature(obj['extractionId'])
        payload = {
            'list': '\n'.join([rg.gene.name for rg in sig.gene_lists[2].ranked_genes]),
            'description': ''
        }
        resp = requests.post('http://amp.pharm.mssm.edu/Enrichr/addList', files=payload)
        if resp.ok:
            new_id = json.loads(resp.text)['userListId']
            new_col = sig.soft_file.dataset.title
            if new_col in columns:
                columns[new_col] += 1
                new_col = '%s_%s' % (new_col, columns[new_col])
            else:
                columns[new_col] = 1

            user_list_ids.append({
                'col_title': new_col,
                'user_list_id': new_id
            })

    return jsonify({
        'background_type': request.json['backgroundType'],
        'user_list_ids': user_list_ids
    })
