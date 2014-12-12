"""This module API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import mimetypes
import sys

import flask

import geodownloader
import diffexp
import softparser
import enrichrlink
from crossdomain import crossdomain
from requestparams import RequestParams

import pdb
import json


ENTRY_POINT = '/g2e'
ERROR_KEY = 'error'

app = flask.Flask(__name__)
app.debug = True

# This forces the browser to download txt files rather than rendering them.
# http://stackoverflow.com/a/3749395/1830334
mimetypes.add_type('application/x-please-download-me', '.txt')


@app.route(ENTRY_POINT)
@crossdomain(origin='*')
def index_endpoint():
	return flask.jsonify({
		'status': 'OK'
	})


@app.route(ENTRY_POINT + '/dlgeo')
@crossdomain(origin='*')
def dlgeo_endpoint():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	rp = RequestParams(flask.request.args)
	#try:
	downloaded_file = geodownloader.download(rp.accession, rp.metadata)
	return flask.jsonify(downloaded_file.__dict__)
	#except IOError as e:
	#	return flask.jsonify({
	#		ERROR_KEY: str(e)
	#	})


@app.route(ENTRY_POINT + '/diffexp')
@crossdomain(origin='*')
def diffexp_endpoint():
	"""Analyzes an existing SOFT file on the server."""

	rp = RequestParams(flask.request.args)
	try:
		control_values,\
		experimental_values,\
		genes,\
		conversion_pct = softparser.parse(rp.filename, rp.metadata.platform, rp.control_names, rp.experimental_names)
	except (LookupError, IOError) as e:
		return flask.jsonify({
			ERROR_KEY: str(e)
		})

	try:
		return flask.jsonify({
			'scores': diffexp.analyze(control_values, experimental_values, genes, rp.config)
		})
	except MemoryError as e:
		return flask.jsonify({
			ERROR_KEY: str(e)
		})
	#return 'success!'


@app.route(ENTRY_POINT + '/enrichr')
@crossdomain(origin='*')
def enrichr_endpoint():
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