# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


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


@app.route('/')
@crossdomain(origin='*')
def index():
	return 'It works!'


@app.route('/dlgeo')
@crossdomain(origin='*')
def dlgeo():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	
	rp = RequestParams(flask.request.args)
	downloaded_file = geodownloader.download_geo_file(rp.accession, rp.options, rp.metadata)
	return flask.jsonify(downloaded_file)


@app.route('/diffexp')
@crossdomain(origin='*')
def diffexp():
	"""Analyzes an existing SOFT file on the server."""

	rp = RequestParams(flask.request.args)
	geo_file_obj = geoanalyzer.analyze_geo_file(rp.filename, rp.options, rp.control, rp.experimental)	
	return flask.jsonify(geo_file_obj)


@app.route('/enrichr')
@crossdomain(origin='*')
def enrichr():
	"""Parses any files on the server and returns a valid Enrichr link
	"""

	rp = RequestParams(flask.request.args)
	enrichr_link = enrichrlink.get_link(rp.filename)
	return flask.jsonify(enrichr_link)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 5000
	if len(sys.argv) > 2:
		host = sys.argv[2]
	else:
		host = '0.0.0.0'
	app.run(port=port, host=host)