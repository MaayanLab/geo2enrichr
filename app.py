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
from requestparams import RequestParams
import softparser


app = flask.Flask(__name__)
app.debug = True


# In production, Apache HTTPD handles serving static files.
if app.debug:
	# This forces the browser to download txt files rather than rendering
	# them. See http://stackoverflow.com/a/3749395/1830334.
	import mimetypes
	mimetypes.add_type('application/x-please-download-me', '.txt')


ENTRY_POINT = '/g2e'


@app.route(ENTRY_POINT)
@crossdomain(origin='*', methods=['GET'])
def index_endpoint():
	return flask.jsonify({
		'status': 'ok',
		'message': ''
	})


@app.route(ENTRY_POINT + '/dlgeo', methods=['POST'])
@crossdomain(origin='*')
def dlgeo_endpoint():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	rp = RequestParams(flask.request.args)
	downloaded_file = geodownloader.download(rp.accession, rp.metadata)
	return flask.jsonify(downloaded_file.__dict__)


@app.route(ENTRY_POINT + '/diffexp', methods=['POST'])
@crossdomain(origin='*')
def diffexp_endpoint():
	"""Parses an existing SOFT file on the server, analyzes the contents for
	differentially expressed genes, and writes the gene list and pvalues to
	new .txt files.
	"""

	rp = RequestParams(flask.request.args)

	# Return early if the platform is not supported.
	if not softparser.platform_supported(rp.metadata.platform):
		return flask.jsonify({
			'status': 'error',
			'message': 'Platform ' + rp.metadata.platform + ' is not supported.'
		})

	# * WARNING *
	#
	# The contents of this try/except are the most complicated part of the
	# program. It is mission critical that these function works as
	# expected: parsing, cleaning, differentially expressing, and
	# averaging the data correctly.

	# Step 1: Parse soft file.
	# Also discard bad data and convert probe IDs to gene symbols.
	A, B, genes, conversion_pct = softparser.parse(rp.filename, rp.metadata.platform, rp.A_cols, rp.B_cols)

	# Step 2: Clean data.
	# Also, if necessary, take log2 of data and quantile normalize it.
	A, B, genes = cleaner.normalize(A, B, genes)

	# Step 3: Identify differential expression.
	gene_pvalue_pairs = diffexper.analyze(A, B, genes, rp.config, rp.filename)

	# Step 4: Generate output files and return to user.
	output_files = filewriter.output_gene_pvalue_pairs(rp.filename, gene_pvalue_pairs)
	output_files['status'] = 'ok'
	output_files['conversion_pct'] = str(conversion_pct)

	# ! TODO !
	# Output filename should be put into database with identifier and returned
	# ID should be returned to user.

	return flask.jsonify(output_files)


@app.route(ENTRY_POINT + '/enrichr', methods=['POST'])
@crossdomain(origin='*')
def enrichr_endpoint():
	"""Parses any files on the server and returns a valid Enrichr link.
	"""

	rp = RequestParams(flask.request.args)
	return flask.jsonify({
		'status': 'ok',
		'up': enrichrlink.get_link(rp.up, rp.up.split('.')[0]),
		'down': enrichrlink.get_link(rp.down, rp.down.split('.')[0]),
		'combined': enrichrlink.get_link(rp.combined, rp.combined.split('.')[0])
	})


@app.route(ENTRY_POINT + '/count', methods=['GET'])
@crossdomain(origin='*')
def count_entpoint():
	"""Returns the number of gene lists that have been extracted from GEO.
	"""

	return flask.jsonify({
		'status': 'ok',
		'extraction_count': db.get_extraction_count()
	})


@app.route(ENTRY_POINT + '/diseases', methods=['GET'])
@crossdomain(origin='*')
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
