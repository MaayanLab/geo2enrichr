"""This module API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Andrew Rouillard, Matthew Jones, Avi Ma'ayan"
__contact__ = "avi.maayan@mssm.edu"
"""


import mimetypes
import sys

import flask

import geodownloader
import geoanalyzer
import enrichrlink
from crossdomain import crossdomain

from requestparams import RequestParams


app = flask.Flask(__name__)
app.debug = True

# This forces the browser to download txt files rather than rendering them.
# http://stackoverflow.com/a/3749395/1830334
mimetypes.add_type('application/x-please-download-me', '.txt')


@app.route('/g2e')
@crossdomain(origin='*')
def index():
	return flask.jsonify({
		'status': 'OK'
	})


@app.route('/g2e/dlgeo')
@crossdomain(origin='*')
def dlgeo():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	rp = RequestParams(flask.request.args)
	downloaded_file = geodownloader.download(rp.accession, rp.metadata)
	return flask.jsonify(downloaded_file.__dict__)


@app.route('/g2e/diffexp')
@crossdomain(origin='*')
def diffexp():
	"""Analyzes an existing SOFT file on the server."""

	rp = RequestParams(flask.request.args)
	geo_file_obj = softanalyzer.analyze(rp.filename, rp.options, rp.control, rp.experimental)	
	return flask.jsonify(geo_file_obj.__dict__)


@app.route('/g2e/enrichr')
@crossdomain(origin='*')
def enrichr():
	"""Parses any files on the server and returns a valid Enrichr link.
	"""

	rp = RequestParams(flask.request.args)
	enrichr_link = enrichrlink.get_link(rp.filename)
	return flask.jsonify(enrichr_link)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		# Defined by AMP
		port = 8083
	if len(sys.argv) > 2:
		host = sys.argv[2]
	else:
		host = '0.0.0.0'
	app.run(port=port, host=host)