"""This module starts the g2e server and handles all valid, incoming requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os
import sys
import flask

from g2e.core.util.crossdomain import crossdomain
from g2e.core.extraction.extractionmaker import extraction_maker
from g2e.core.softfile.softparser import PROBE2GENE


app = flask.Flask(__name__, static_url_path='')


ALLOWED_ORIGINS = '*'
ENTRY_POINT = '/g2e'
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'


# http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request

# curl --data "dataset=GDS5077&platform=GPL10558&A_cols=GSM1071454,GSM1071455&B_cols=GSM1071457,GSM1071455" http://localhost:8083/g2e/api/extract/geo
# curl --form "file=@tests/data/chdir_input.txt" --form name=Neil http://localhost:8083/g2e/api/extract/upload


@app.route(ENTRY_POINT + '/', methods=['GET'])
@crossdomain(origin='*')
def index():
    directory = SERVER_ROOT + '/web/site'
    return flask.send_from_directory(directory, 'index.html')


# PURPLE_WIRE: Apache should serve these files.
@app.route(ENTRY_POINT + '/<path:path>')
@crossdomain(origin='*')
def send_static(path):
    subdir = '' if 'static' in path else '/web/site'
    directory = SERVER_ROOT + subdir
    return flask.send_from_directory(directory, path)


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
                response['error'] = 'Platform not supported.'
            else:
                response['extraction_id'] = extraction_maker(args=flask.request.form)
        else:
            flask.jsonify({
                'error': 'Invalid API endpoint'
            })
    elif flask.request.method == 'GET':
        response = extraction_maker(id=path)

    return flask.jsonify(response)
