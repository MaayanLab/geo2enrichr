"""API for hierarchical clustering.
"""

import requests
import json
from flask import Blueprint, redirect, request, jsonify

from substrate import TargetApp
from substrate import TargetAppLink

from g2e.db import dataaccess
from g2e.db.util import get_or_create
from g2e.core.cluster import cluster
from g2e.config import Config

cluster_api = Blueprint('cluster_api',
                        __name__,
                        url_prefix='%s/cluster' % Config.BASE_URL)


@cluster_api.route('/<extraction_id>', methods=['GET'])
def perform_hierarchical_clustering(extraction_id):
    """Performs hierarchical clustering on a SOFT file.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    target_app_link = _get_clustergrammer_link(gene_signature)

    # Only create the link from Clustergrammer once.
    if not target_app_link:
        link = cluster.from_soft_file(gene_signature)
        target_app = get_or_create(TargetApp, name='clustergrammer')
        target_app_link = TargetAppLink(target_app, link)
        gene_signature.gene_lists[2].target_app_links.append(
            target_app_link
        )
        dataaccess.save_gene_signature(gene_signature)

    return redirect(target_app_link.link)


def _get_clustergrammer_link(gene_signature):
    for target_app_link in gene_signature.gene_lists[2].target_app_links:
        if target_app_link.target_app.name == 'clustergrammer':
            return target_app_link
