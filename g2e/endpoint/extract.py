"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, request, jsonify
from flask.ext.cors import cross_origin
from g2e.app.config import BASE_API_URL
from g2e.dao import extractiondao
from g2e.model.extraction import Extraction


extract = Blueprint('api', __name__, url_prefix=BASE_API_URL + '/extract')


@extract.route('/<path>', methods=['GET', 'POST'])
@cross_origin()
def extract_endpoint(path):
    """Single entry point for extracting a gene list from a SOFT file.
    """
    if request.method == 'POST':
        return do_post()
    elif request.method == 'GET':
        return do_get(path)


def do_post(path):
    """Handle POST requests, which are to two endpoints: upload or geo.
    """
    response = {}
    if path == 'upload':
        extraction = Extraction.from_file(request.files['file'], request.form)
    elif path == 'geo':
        extraction = Extraction.from_geo(request.form)
    extractiondao.save(extraction)
    response['extraction_id'] = extraction.extraction_id
    return jsonify(response)


def do_get(path):
    """Handle GET request based on extraction ID.
    """
    extraction = extractiondao.fetch(path)
    response = extraction.serialize
    return jsonify(response)