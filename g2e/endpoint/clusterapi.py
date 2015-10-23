"""Delegates to hierarchical clustering module.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template, request
import json

from g2e.core.cluster import cluster
from g2e.config import Config
from g2e.dataaccess import dataaccess


cluster_blueprint = Blueprint('cluster', __name__, url_prefix=Config.BASE_URL + '/cluster')


@cluster_blueprint.route('<extraction_id>', methods=['GET'])
def perform_hierarchical_clustering(extraction_id):
    """Performs hierarchical clustering on a SOFT file.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    x = cluster.from_soft_file(gene_signature.soft_file)
    return x
