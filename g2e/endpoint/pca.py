"""Builds a GeneList file upon request.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, Response
from g2e.config import Config
from g2e.dataaccess import dataaccess


pca = Blueprint('pca', __name__, url_prefix=Config.BASE_URL + '/pca')


@pca.route('/<extraction_id>')
def perform_pca(extraction_id):
    """Performs PCA analysis on a SOFT file, referenced by gene signature
    extraction_id.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    if gene_signature:
        return 'hello'
