"""This module has the API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import mimetypes
import sys
import urllib2

import flask

import cleaner
from crossdomain import crossdomain
import diffexper
import enrichrlink
import geodownloader
import filewriter
from requestparams import RequestParams
import softparser


app = flask.Flask(__name__)
app.debug = True

# This forces the browser to download txt files rather than rendering them.
# http://stackoverflow.com/a/3749395/1830334
mimetypes.add_type('application/x-please-download-me', '.txt')


ENTRY_POINT = '/g2e'


@app.route(ENTRY_POINT)
@crossdomain(origin='*')
def index_endpoint():
	return flask.jsonify({
		'status': 'ok',
		'message': ''
	})


@app.route(ENTRY_POINT + '/dlgeo')
@crossdomain(origin='*')
def dlgeo_endpoint():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.
	rp = RequestParams(flask.request.args)
	try:
		downloaded_file = geodownloader.download(rp.accession, rp.metadata)
		return flask.jsonify(downloaded_file.__dict__)
	except IOError as e:
		return flask.jsonify({
			'status': 'error',
			'message': str(e)
		})


@app.route(ENTRY_POINT + '/diffexp')
@crossdomain(origin='*')
def diffexp_endpoint():
	"""Parses an existing SOFT file on the server, analyzes the contents for
	differentially expressed genes, and writes the gene list and pvalues to
	new .txt files.
	"""

	rp = RequestParams(flask.request.args)
	try:
		# ! WARNING !
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
	except (LookupError, IOError, MemoryError, ValueError, StopIteration) as e:
		return flask.jsonify({
			'error': str(e)
		})

	output_file = filewriter.output_gene_pvalue_pairs(rp.filename, gene_pvalue_pairs, rp.config['inclusion'])

	return flask.jsonify({
		'status': 'ok',
		'conversion_pct': str(conversion_pct),
		'filename': str(output_file)
	})


@app.route(ENTRY_POINT + '/enrichr')
@crossdomain(origin='*')
def enrichr_endpoint():
	"""Parses any files on the server and returns a valid Enrichr link.
	"""

	rp = RequestParams(flask.request.args)
	# Sometimes this takes a while or Enrichr is down. We do not want to
	# prevent users from being able to download their files.
	try:
		#link = enrichrlink.get_link(rp.filename)
		return flask.jsonify({
			'status': 'ok',
			'link': 'TODO'
		})
	except urllib2.HTTPError as e:
		return flask.jsonify({
			'status': 'error',
			'message': str(e)
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