"""Delegates to hierarchical clustering module.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import requests
import json
from flask import Blueprint, redirect, request, jsonify

from g2e.core.cluster import cluster
from g2e.config import Config
from g2e.dataaccess import dataaccess
from g2e.model.targetapp import TargetApp
from g2e.model.targetapplink import TargetAppLink
from g2e.dataaccess.util import get_or_create


cluster_blueprint = Blueprint('cluster', __name__, url_prefix=Config.BASE_URL + '/cluster')


CLUSTERGRAMMER_URL = 'http://amp.pharm.mssm.edu/clustergrammer/g2e/'


@cluster_blueprint.route('/<extraction_id>', methods=['GET'])
def perform_hierarchical_clustering(extraction_id):
    """Performs hierarchical clustering on a SOFT file.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    target_app_link = _get_clustergrammer_link(gene_signature)

    # Ensure we only create the link from Clustergrammer once.
    if not target_app_link:
        link = cluster.from_soft_file(gene_signature)
        target_app = get_or_create(TargetApp, name='clustergrammer')
        target_app_link = TargetAppLink(target_app, link)
        gene_signature.gene_lists[2].target_app_links.append(
            target_app_link
        )
        dataaccess.save_gene_signature(gene_signature)

    return redirect(target_app_link.link)


@cluster_blueprint.route('/enrichr', methods=['POST'])
def enrichr_to_clustergrammer():
    """Based on extraction IDs, gets enrichment vectors from Enrichr
    and then creates a hierarchical cluster from Clustergrammer.
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


@cluster_blueprint.route('/l1000cds2', methods=['POST'])
def l1000cds2_to_clustergrammer():
    """Based on extraction IDs, gets enrichment vectors from Enrichr
    and then creates a hierarchical cluster from Clustergrammer.
    """
    mimic = request.json['mode'] == 'Mimic'
    samples = []
    i = 0
    for obj in request.json['signatures']:
        try:
            i += 1
            print(obj)

            sig = dataaccess.fetch_gene_signature(obj['extractionId'])
            url = 'http://amp.pharm.mssm.edu/L1000CDS2/query'
            headers = { 'content-type': 'application/json' }
            payload = {
                'data': {
                    'genes': [rg.gene.name for rg in sig.gene_lists[2].ranked_genes],
                    'vals': [rg.value for rg in sig.gene_lists[2].ranked_genes]
                },
                'config': {
                    'aggravate': mimic,
                    'searchMethod': 'CD',
                    'share': False,
                    'combination': False,
                    'db-version': 'latest'
                },
                'metadata': []
            }
            resp = requests.post(url, data=json.dumps(payload), headers=headers)
            perts = []
            scores = []
            for obj in json.loads(resp.text)['topMeta']:
                desc_temp = obj['pert_desc']
                if desc_temp == '-666':
                    print('using broad id: ' + str(obj['pert_id']))
                    desc_temp = obj['pert_id']
                desc = '%s - %s' % (desc_temp, obj['cell_id'])
                perts.append(desc)
                # L1000CDS^2 gives scores from 0 to 2. With mimic, low scores are
                # better; with reverse, high scores are better. If we subtract
                # this score from 1, we get a negative value for reverse and a
                # positive value for mimic.
                score = 1 - obj['score']
                scores.append(score)

            samples.append({
                'col_title': sig.soft_file.dataset.accession + '_' + str(i),
                'link': 'todo',
                'genes': [[x,y] for x,y in zip(perts, scores)],
                'name': 'todo'
            })
        except Exception as e:
            print('error: ' + str(e))
            continue

    payload = {
        'link': 'todo',
        'gene_signatures': samples
    }

    headers = { 'content-type': 'application/json' }
    sess = requests.session()
    resp = sess.post(CLUSTERGRAMMER_URL, data=json.dumps(payload), headers=headers)
    if resp.ok:
        return jsonify({
            'link': json.loads(resp.text)['link']
        })
    else:
        return jsonify({
            'link': 'error'
        })


def _get_clustergrammer_link(gene_signature):
    for target_app_link in gene_signature.gene_lists[2].target_app_links:
        if target_app_link.target_app.name == 'clustergrammer':
            return target_app_link
