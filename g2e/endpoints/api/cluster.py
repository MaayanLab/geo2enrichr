"""API for hierarchical clustering.
"""

from flask import Blueprint

from g2e.core.targetapp import clustergrammer
from g2e.config import Config
from g2e.db import dataaccess

cluster_api = Blueprint('cluster_api',
                        __name__,
                        url_prefix='%s/cluster' % Config.BASE_URL)


@cluster_api.route('/<extraction_id>', methods=['GET'])
def perform_hierarchical_clustering(extraction_id):
    """Performs hierarchical clustering on a SOFT file.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    return clustergrammer.from_soft_file(gene_signature)
