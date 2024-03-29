"""API for performing principal component analysis.
"""

import json

from flask import Blueprint, render_template
from g2e import config, database, pca

pca_api = Blueprint('pca_api',
                    __name__,
                    url_prefix='%s/pca' % config.BASE_URL)


@pca_api.route('/<extraction_id>', methods=['GET'])
def perform_soft_file_pca(extraction_id):
    """Performs PCA on a SOFT file, referenced by extraction_id.
    """
    gene_signature = database.get_gene_signature(extraction_id)
    if gene_signature:
        pca_data = pca.from_soft_file(gene_signature.soft_file)
        pca_json = json.dumps(pca_data)
        return render_template('pages/pca.html',
                               pca_data=pca_json,
                               results_url=config.RESULTS_URL,
                               extraction_id=gene_signature.extraction_id)
