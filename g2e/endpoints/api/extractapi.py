"""API for extracting gene signatures from GEO and custom datasets.
"""

from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin

from g2e.db import dataaccess
from g2e.core import genesignature
from g2e.config import Config
import g2e.core.softutils.filemanager as softfilemanager

extract_api = Blueprint('extract_api',
                        __name__,
                        url_prefix='%s/extract' % Config.BASE_API_URL)


@extract_api.route('/<extraction_id>')
@cross_origin()
def get_extraction(extraction_id):
    """Handles GET request based on extraction ID.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
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
    gene_signature = genesignature.from_geo(args)
    dataaccess.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload', methods=['POST'])
@cross_origin()
def post_file():
    """Handles POST file upload.
    """
    args = request.form
    response = {}
    gene_signature = genesignature.from_file(request.files['file'], args)
    dataaccess.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/example', methods=['POST'])
@cross_origin()
def example_file():
    """Handles an example SOFT file extraction.
    """
    args = request.form
    response = {}
    file_obj = softfilemanager.get_example_file()
    gene_signature = genesignature.from_file(file_obj, args)
    dataaccess.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)
