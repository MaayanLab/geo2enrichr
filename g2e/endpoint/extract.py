"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin
from g2e.config import Config
from g2e.dataaccess import dataaccess
from g2e.model.extraction import Extraction


extract = Blueprint('api', __name__, url_prefix=Config.BASE_API_URL + '/extract')


@extract.route('/<extraction_id>')
@cross_origin()
def get_extraction(extraction_id):
    """Handle GET request based on extraction ID.
    """
    extraction = dataaccess.fetch_extraction(extraction_id)
    if extraction is None:
        return jsonify({
            'error': 'No gene signatures with ID %s found' % extraction_id
        })
    else:
        return jsonify(extraction.serialize)


@extract.route('/geo', methods=['POST'])
@cross_origin()
def post_from_geo():
    """Handle POST requests from GEO.
    """
    response = {}
    extraction = Extraction.from_geo(request.form)
    dataaccess.save_extraction(extraction)
    response['extraction_id'] = extraction.extraction_id
    return jsonify(response)


@extract.route('/upload', methods=['POST'])
@cross_origin()
def post_file():
    """Handle POST file upload.
    """
    response = {}
    extraction = Extraction.from_file(request.files['file'], request.form)
    dataaccess.save_extraction(extraction)
    response['extraction_id'] = extraction.extraction_id
    return jsonify(response)



