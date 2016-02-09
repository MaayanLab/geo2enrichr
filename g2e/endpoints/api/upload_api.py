"""API for uploading pre-existing gene signatures, i.e. does not perform
differential expression analysis.
"""

import json

from flask import Blueprint, jsonify, request

from g2e import config, signature_factory, database


upload_api = Blueprint('upload_api',
                       __name__,
                       url_prefix=config.UPLOAD_URL)


@upload_api.route('/', methods=['POST'])
def upload_gene_signature():
    """Uploads gene signature and returns extraction ID.
    """
    args = json.loads(request.data)
    gene_signature = signature_factory.from_gene_list(args)
    database.save_gene_signature(gene_signature)
    return jsonify({
        'extraction_id': gene_signature.extraction_id,
        'link': ''
    })
