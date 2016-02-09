"""API for extracting gene signatures from GEO and custom datasets.
"""

from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin

from g2e import config, db
from g2e import signaturefactory


extract_api = Blueprint('extract_api',
                        __name__,
                        url_prefix=config.EXTRACT_URL)


@extract_api.route('/<extraction_id>')
@cross_origin()
def get_extraction(extraction_id):
    """Handles GET request based on extraction ID.
    """
    gene_signature = db.get_gene_signature(extraction_id)
    if gene_signature is None:
        return jsonify({
            'error': 'No gene signatures with ID %s found' % extraction_id
        })
    else:
        return jsonify(gene_signature.serialize)


@extract_api.route('/geo', methods=['POST'])
@cross_origin()
def post_from_geo():
    """Handles POST requests from GEO.
    """
    args = request.form
    response = {}
    gene_signature = signaturefactory.from_geo(args)
    db.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload', methods=['POST'])
@cross_origin()
def post_file():
    """Handles POST file upload.
    """
    args = request.form
    response = {}
    gene_signature = signaturefactory.from_file(request.files['file'], args)
    db.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/example', methods=['POST'])
@cross_origin()
def example_file():
    """Handles an example SOFT file extraction.
    """
    args = request.form
    response = {}
    file_obj = signaturefactory.get_example_file()
    gene_signature = signaturefactory.from_file(file_obj, args)
    db.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)
