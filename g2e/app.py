"""This module starts the g2e server and handles all valid, incoming requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os
import sys
import flask
# Allows for logging data to Apache's logs.
import logging
logging.basicConfig(stream=sys.stderr)

from g2e.core.util.crossdomain import crossdomain
from g2e.core.extraction.extractionmaker import extraction_maker
from g2e.core.softfile.softparser import PROBE2GENE


app = flask.Flask(__name__, static_url_path='')


ALLOWED_ORIGINS = '*'
ENTRY_POINT = '/g2e'
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'


@app.route(ENTRY_POINT + '/', methods=['GET'])
@crossdomain(origin='*')
def index():
    return flask.send_from_directory(SERVER_ROOT + '/web/site', 'index.html')


# PURPLE_WIRE: Apache should serve these files.
@app.route(ENTRY_POINT + '/<path:path>')
@crossdomain(origin='*')
def send_static(path):
    return flask.send_from_directory(SERVER_ROOT, path)


@app.route(ENTRY_POINT + '/api/extract/<path>', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def extract(path):
    """Single entry point for extracting a gene list from a SOFT file.
    Delegates to constructors that handle data processing and further
    delegation to the DAO and ORM.
    """
    response = {}
    if flask.request.method == 'PUT' or flask.request.method == 'POST':
        if path == 'upload':
            response['extraction_id'] = extraction_maker(
                file = flask.request.files['file'],
                args = flask.request.form
            )
        elif path == 'geo':
            if flask.request.form.get('platform') not in PROBE2GENE:
                flask.abort(400)
            else:
                response['extraction_id'] = extraction_maker(args=flask.request.form)
        else:
            flask.jsonify({
                'error': 'Invalid API endpoint'
            })
    elif flask.request.method == 'GET':
        response = extraction_maker(id=path)

    return flask.jsonify(response)
