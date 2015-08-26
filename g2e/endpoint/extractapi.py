"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin
from g2e.config import Config
from g2e.dataaccess import dataaccess
from g2e.model.genesignature import GeneSignature


extract_api = Blueprint('extract_api', __name__, url_prefix=Config.BASE_API_URL + '/extract')


@extract_api.route('/<extraction_id>')
@cross_origin()
def get_extraction(extraction_id):
    """Handle GET request based on extraction ID.
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
    """Handle POST requests from GEO.
    """
    args = request.form
    response = {}
    gene_signature = GeneSignature.from_geo(args)
    dataaccess.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload', methods=['POST'])
@cross_origin()
def post_file():
    """Handle POST file upload.
    """
    args = request.form
    response = {}
    gene_signature = GeneSignature.from_file(request.files['file'], args)
    dataaccess.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)



