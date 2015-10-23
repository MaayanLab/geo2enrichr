"""Performs PCA on a list of gene signatures or a SOFT file.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template, request
import json

from g2e.core.pca import pca
from g2e.config import Config
from g2e.dataaccess import dataaccess


pca_blueprint = Blueprint('pca', __name__, url_prefix=Config.BASE_URL + '/pca')


@pca_blueprint.route('', methods=['POST'])
def perform_gene_signatures_pca():
    """Performs PCA on a list of gene signatures, referenced by extraction_id.
    """
    pca_data = pca.from_gene_signatures(request.json)
    return pca_data


@pca_blueprint.route('/<extraction_id>', methods=['GET'])
def perform_soft_file_pca(extraction_id):
    """Performs PCA on a SOFT file, referenced by extraction_id.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    if gene_signature:
        pca_data = pca.from_soft_file(gene_signature.soft_file)
        pca_json = json.dumps(pca_data)
        return render_template('pca.html',
                               pca_data=pca_json,
                               results_url=Config.BASE_RESULTS_URL,
                               extraction_id=gene_signature.extraction_id)
