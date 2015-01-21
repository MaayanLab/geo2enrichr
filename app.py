"""This module has the API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sys

import flask

import cleaner
from crossdomain import crossdomain
import db
import diffexper
import enrichrlink
import geodownloader
import filewriter
import json
from request import RequestArgs
from response import make_json_response
import softparser


app = flask.Flask(__name__)
app.debug = True


# In production, Apache HTTPD handles serving static files.
if app.debug:
	# This forces the browser to download txt files rather than rendering
	# them. See http://stackoverflow.com/a/3749395/1830334.
	import mimetypes
	mimetypes.add_type('application/x-please-download-me', '.txt')


ALLOWED_ORIGINS = '*'
ENTRY_POINT = '/g2e'


@app.route(ENTRY_POINT, methods=['GET'])
@crossdomain(origin='*')
def index_endpoint():
	return flask.jsonify({
		'status': 'ok',
		'message': ''
	})


@app.route(ENTRY_POINT + '/dlgeo', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def dlgeo_endpoint():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	args = RequestArgs(flask.request.json)
	downloaded_file = geodownloader.download(args.accession, args.metadata)
	return make_json_response(downloaded_file.__dict__)


@app.route(ENTRY_POINT + '/diffexp', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def diffexp_endpoint():
	"""Parses an existing SOFT file on the server, analyzes the contents for
	differentially expressed genes, and writes the gene list and pvalues to
	new .txt files.
	"""

	args = RequestArgs(flask.request.json)

	# Return early if the platform is not supported.
	if not softparser.platform_supported(args.metadata.platform):
		return make_json_response({
			'status': 'error',
			'message': 'Platform ' + args.metadata.platform + ' is not supported.'
		})

	# * WARNING *
	#
	# The contents of this try/except are the most complicated part of the
	# program. It is mission critical that these function works as
	# expected: parsing, cleaning, differentially expressing, and
	# averaging the data correctly.

	# Step 1: Parse soft file.
	# Also discard bad data and convert probe IDs to gene symbols.
	A, B, genes, conversion_pct = softparser.parse(args.filename, args.metadata.platform, args.A_cols, args.B_cols)

	# Step 2: Clean data.
	# Also, if necessary, take log2 of data and quantile normalize it.
	A, B, genes = cleaner.normalize(A, B, genes)

	# Step 3: Identify differential expression.
	gene_pvalue_pairs = diffexper.analyze(A, B, genes, args.config, args.filename)

	# Step 4: Generate output files and return to user.
	output_files = filewriter.output_gene_pvalue_pairs(args.filename, gene_pvalue_pairs)
	output_files['status'] = 'ok'
	output_files['conversion_pct'] = str(conversion_pct)

	# ! TODO !
	# Output filename should be put into database with identifier and returned
	# ID should be returned to user.
	db.record_extraction('GDS5077', args.A_cols, args.B_cols, args.metadata, args.config)

	return make_json_response(output_files)


@app.route(ENTRY_POINT + '/enrichr', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def enrichr_endpoint():
	"""Parses any files on the server and returns a valid Enrichr link.
	"""

	args = RequestArgs(flask.request.json)
	return flask.jsonify({
		'status': 'ok',
		'up': enrichrlink.get_link(args.up, args.up.split('.')[0]),
		'down': enrichrlink.get_link(args.down, args.down.split('.')[0]),
		'combined': enrichrlink.get_link(args.combined, args.combined.split('.')[0])
	})


@app.route(ENTRY_POINT + '/count', methods=['GET'])
@crossdomain(origin=ALLOWED_ORIGINS)
def count_entpoint():
	"""Returns the number of gene lists that have been extracted from GEO.
	"""

	return flask.jsonify({
		'status': 'ok',
		'extraction_count': db.get_extraction_count()
	})


@app.route(ENTRY_POINT + '/diseases', methods=['GET'])
@crossdomain(origin=ALLOWED_ORIGINS)
def rare_diseases_endpoint():
	"""Returns a list of rare diseases.
	"""

	return flask.jsonify({
		'status': 'ok',
		'rare_diseases': db.get_rare_diseases()
	})


# This error handler should only be used for truly *exceptional* scenarios,
# i.e. scenarios you do *not* expect to happen. If you can predict a program
# flow, handle it by returnning valid JSON with "'status': 'error'".
@app.errorhandler(Exception)
def server_error(err):
	return flask.jsonify({
		'status': 'error',
		'message': 'Unknown server-side error. Please document your input and contact the Ma\'ayan Lab'
	})


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
