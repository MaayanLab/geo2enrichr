"""This module starts the g2e server and handles all valid, incoming requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os
import time
import sys
import flask

from g2e.core.util.crossdomain import crossdomain
from g2e.core.extraction.extractionmaker import extraction_maker


app = flask.Flask(__name__, static_url_path='')


ALLOWED_ORIGINS = '*'
ENTRY_POINT = '/g2e'
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'


# http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request

# curl --data "dataset=GDS5077&platform=GPL10558&A_cols=GSM1071454,GSM1071455&B_cols=GSM1071457,GSM1071455" http://localhost:8083/g2e/extract
# curl --form "file=@tests/data/chdir_input.txt" --form name=Neil http://localhost:8083/g2e/extract


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


@app.route(ENTRY_POINT + '/extract', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def extract():
    """Single entry point for extracting a gene list from a SOFT file.
    Delegates to constructors that handle data processing and further
    delegation to the DAO and ORM.
    """
    response = {}
    if flask.request.method == 'PUT' or flask.request.method == 'POST':
        if flask.request.files:
            response['extraction_id'] = extraction_maker(
                file = flask.request.files['file'],
                args = flask.request.form
            )
        else:
            response['extraction_id'] = extraction_maker(args=flask.request.form)
    elif flask.request.method == 'GET':
        s = time.time()
        extraction = extraction_maker(id=flask.request.args.get('id'))
        response = clean_extraction(extraction)
        response['time'] = time.time() - s

    return flask.jsonify(response)


def clean_extraction(extraction):
    response = extraction.__dict__
    response['softfile'] = extraction.softfile.__dict__
    response['genelists'] = [gl.__dict__ for gl in extraction.genelists]
    response['metadata'] = extraction.metadata.__dict__
    del response['genelists'][0]['ranked_genes']
    del response['genelists'][1]['ranked_genes']
    # Leave the combined genes?
    #del response['genelists'][2]['ranked_genes']
    del response['softfile']['A']
    del response['softfile']['A_cols']
    del response['softfile']['B']
    del response['softfile']['B_cols']
    del response['softfile']['genes']
    return response


#if __name__ == '__main__':
#    # This is only for local development. For Apache, the application is
#    # imported and run from another module.
#    port = 8083
#    host = '0.0.0.0'
#    app.run(port=port, host=host)
