"""Handles default Responses from the server.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import json

import flask


def get_flask_json_response(data):

	resp = flask.Response(json.dumps(data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
