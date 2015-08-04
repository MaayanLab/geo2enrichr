"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, request, abort, jsonify
from g2e.core.util.crossdomain import crossdomain
from g2e.core.softfile.softparser import PROBE2GENE
from g2e.app.config import BASE_URL
from g2e.dao import dao
from g2e.model.extraction import Extraction


api = Blueprint('api', __name__, url_prefix=BASE_URL + '/api')


# TODO: Break this into multiple endpoints, rather than using conditionals.
@api.route('/extract/<path>', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def api_endpoint(path):
    """Single entry point for extracting a gene list from a SOFT file.
    """
    response = {}
    if request.method == 'PUT' or request.method == 'POST':
        if path == 'upload':
            extraction = Extraction.from_file(request.files['file'], request.form)
        elif path == 'geo':
            extraction = Extraction.from_geo(request.form)
        dao.save(extraction)
        response['extraction_id'] = extraction.extraction_id
    elif request.method == 'GET':
        extraction = dao.fetch(path)
        response = extraction.serialize
    return jsonify(response)