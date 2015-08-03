"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, request, abort, jsonify
from g2e.core.util.crossdomain import crossdomain
from g2e.core.extraction.extractionmaker import extraction_maker
from g2e.core.softfile.softparser import PROBE2GENE
from g2e.app.config import BASE_URL


api = Blueprint('api', __name__, url_prefix=BASE_URL + '/api')


@api.route('/extract/<path>', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def api_endpoint(path):
    """Single entry point for extracting a gene list from a SOFT file.
    Delegates to constructors that handle data processing and further
    delegation to the DAO and ORM.
    """
    response = {}
    if request.method == 'PUT' or request.method == 'POST':
        if path == 'upload':
            response['extraction_id'] = extraction_maker(
                file = request.files['file'],
                args = request.form
            )
        elif path == 'geo':
            if request.form.get('platform') not in PROBE2GENE:
                abort(400)
            else:
                response['extraction_id'] = extraction_maker(args=flask.request.form)
        else:
            jsonify({
                'error': 'Invalid API endpoint'
            })
    elif request.method == 'GET':
        response = extraction_maker(id=path)

    return jsonify(response)