"""This module has the API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sys
import time

import flask

import cleaner
from crossdomain import crossdomain
import db
import diffexper
import enrichrlink
import geodownloader
from files import GeneFile
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


# TODO: This is an absolutely awful hack that I (GWG) wrote to get the `full`
# endpoint restabilized for a user. Long term, we *must* re-architecture this
# module so that we are more dry.
#
# Nearly every line of code is actually repeated somewhere else in this
# module. Comments should be with the original code.
@app.route(ENTRY_POINT + '/full', methods=['GET'])
@crossdomain(origin='*')
def full_endpoint():

	s = time.time()

	args = RequestArgs(flask.request.args)
	filename = geodownloader.download(args.accession, args.metadata).filename

	A, B, genes, conversion_pct = softparser.parse(filename, args.metadata.platform, args.A_cols, args.B_cols)
	A, B, genes = cleaner.normalize(A, B, genes)

	gene_pvalue_pairs = diffexper.analyze(A, B, genes, args.config, filename)
	output_files = filewriter.output_gene_pvalue_pairs(filename, gene_pvalue_pairs)
	
	accession = filename.split('_')[0]
	db.record_extraction(accession, args.A_cols, args.B_cols, args.metadata, args.config)

	up   = output_files['up']
	down = output_files['down']

	response = {
		'status': 'ok',
		'time': time.time() - s,
		'conversion_pct': str(conversion_pct),
		'up_genes': GeneFile(up).to_dict(include_membership=True),
		'down_genes': GeneFile(down).to_dict(include_membership=True),
	}
	if args.config.cutoff:
		response['up_enrichr'] = enrichrlink.get_link(up, up.split('.')[0])
		response['down_enrichr'] = enrichrlink.get_link(down, down.split('.')[0])
	return flask.jsonify(response)


@app.route(ENTRY_POINT + '/dlgeo', methods=['PUT', 'OPTIONS'])
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

	# TODO: This is a *hack* to get the accession number. This *should* be
	# passed from the front-end or better yet saved in the DB from the
	# previous request--I'm not sure what the architecture should be in this
	# latter scenario.
	accession = args.filename.split('_')[0]
	# Output filename should be put into database with identifier and returned
	# ID should be returned to user.
	db.record_extraction(accession, args.A_cols, args.B_cols, args.metadata, args.config)

	return make_json_response(output_files)


@app.route(ENTRY_POINT + '/enrichr', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def enrichr_endpoint():
	"""Parses files on the server, pipes the results to Enrichr, and returns a
	valid link.
	"""

	args = RequestArgs(flask.request.json)
	# All descriptions should be the same.
	description = args.up.split('.')[0]
	up_link =  enrichrlink.get_link(args.up, description)
	# Do not use Enrichr if the first timeout fails. Assume Enrichr is down.
	down_link = enrichrlink.get_link(args.down, description) if up_link else ''
	combined_link = enrichrlink.get_link(args.combined, description) if up_link else ''

	return flask.jsonify({
		'status': 'ok',
		'up': up_link,
		'down': down_link,
		'combined': combined_link
	})


@app.route(ENTRY_POINT + '/stringify', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def stringify_endpoint():
	"""
	"""

	args = RequestArgs(flask.request.json)
	up_genes = GeneFile(args.up)
	dn_genes = GeneFile(args.down)
	return flask.jsonify({
		'status': 'ok',
		'up': up_genes.to_str('-', False),
		'down': dn_genes.to_str('-', False)
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


@app.route(ENTRY_POINT + '/platforms', methods=['GET'])
@crossdomain(origin=ALLOWED_ORIGINS)
def platforms_endpoint():
	"""Returns a dictionary of support platforms.
	"""

	return flask.jsonify({
		'status': 'ok',
		'supported_platforms': db.get_supported_platforms()
	})


# This error handler should only be used for truly *exceptional* scenarios,
# i.e. scenarios you do *not* expect to happen. If you can predict a program
# flow, handle it by returnning valid JSON with "'status': 'error'".
#@app.errorhandler(Exception)
#def server_error(err):
#	return flask.jsonify({
#		'status': 'error',
#		'message': 'Unknown server-side error. Please document your input and contact the Ma\'ayan Lab'
#	})


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
