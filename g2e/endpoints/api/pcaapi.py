"""API for performing principal component analysis.
"""

import json

from flask import Blueprint, render_template
from g2e.db import dataaccess
from g2e.core import analysis
from g2e.config import Config

pca_api = Blueprint('pca_api',
                    __name__,
                    url_prefix='%s/pca' % Config.BASE_URL)


@pca_api.route('/<extraction_id>', methods=['GET'])
def perform_soft_file_pca(extraction_id):
    """Performs PCA on a SOFT file, referenced by extraction_id.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    if gene_signature:
        pca_data = analysis.pca.from_soft_file(gene_signature.soft_file)
        pca_json = json.dumps(pca_data)
        return render_template('pages/pca.html',
                               pca_data=pca_json,
                               results_url=Config.RESULTS_PAGE_URL,
                               extraction_id=gene_signature.extraction_id)
