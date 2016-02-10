"""API for extracting gene signatures from GEO and custom datasets.
"""

import json

from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin

from g2e import config, database
from g2e import signature_factory


extract_api = Blueprint('extract_api',
                        __name__,
                        url_prefix=config.EXTRACT_URL)


@extract_api.route('/<extraction_id>', methods=['GET'])
@cross_origin()
def get_extraction(extraction_id):
    """Handles GET request based on extraction ID.
    """
    gene_signature = database.get_gene_signature(extraction_id)
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
    gene_signature = signature_factory.from_geo(args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload_soft_file', methods=['POST'])
@cross_origin()
def post_file():
    """Handles POST file upload.
    """
    args = request.form
    response = {}
    gene_signature = signature_factory.from_file(request.files['file'], args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload_gene_list', methods=['POST'])
def upload_gene_list():
    """Uploads gene signature and returns extraction ID.
    """
    args = json.loads(request.data)
    gene_signature = signature_factory.from_gene_list(args)
    database.save_gene_signature(gene_signature)
    link = '%s%s/%s' % (config.SERVER_URL,
                         config.RESULTS_URL,
                         gene_signature.extraction_id)
    return jsonify({
        'extraction_id': gene_signature.extraction_id,
        'link': link
    })


@extract_api.route('/example', methods=['POST'])
@cross_origin()
def example_file():
    """Handles an example SOFT file extraction.
    """
    args = request.form
    response = {}
    file_obj = signature_factory.get_example_file()
    gene_signature = signature_factory.from_file(file_obj, args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)
