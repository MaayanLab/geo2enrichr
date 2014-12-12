"""This module has the API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import mimetypes
import sys
from time import time

import flask

from crossdomain import crossdomain
import diffexper
import enrichrlink
from files import GeneFile
import geodownloader
from requestparams import RequestParams
import softparser

import pdb


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
	try:
		downloaded_file = geodownloader.download(rp.accession, rp.metadata)
		return flask.jsonify(downloaded_file.__dict__)
	except IOError as e:
		return flask.jsonify({
			ERROR_KEY: str(e)
		})


@app.route(ENTRY_POINT + '/diffexp')
@crossdomain(origin='*')
def diffexp_endpoint():
	"""Parses an existing SOFT file on the server, analyzes the contents for
	differentially expressed genes, and writes the gene list and pvalues to
	new .txt files.
	"""

	# Set to -1 to avoid a reference error in case of exception.
	parse_time = diff_exp_time = -1
	rp = RequestParams(flask.request.args)
	try:
		# Parse SOFT file, discarind bad data, averaging duplicates, and
		# bucketing expression data into A, B lists.
		parse_time = time()
		A, B, genes, conversion_pct = softparser.parse(rp.filename, rp.metadata.platform, rp.A_cols, rp.B_cols)
		parse_time = time() - parse_time

		# Identify differentially expressed genes.
		diff_exp_time = time()
		gene_pvalues = diffexper.analyze(A, B, genes, rp.config)
		diff_exp_time = time() - diff_exp_time
	except (LookupError, IOError, MemoryError, ValueError) as e:
		return flask.jsonify({
			ERROR_KEY: str(e)
		})

	return flask.jsonify({
		'timing' : {
			'parse_time': str(parse_time)[:4],
			'diff_exp_time': str(diff_exp_time)[:4]
		},
		'scores': gene_pvalues
	})

	'''
	# Output genes and pvalues to three files on the server and return a
	# reference to them for the client. Also return metrics on data quality
	# and methods used, if necessary.
	filename = rp.filename.replace('.soft', '')
	path_up   = GeneFile(filename, 'up').path()
	path_down = GeneFile(filename, 'down').path()
	path_comb = GeneFile(filename, 'combined').path()
	with open(path_up, 'w') as up_out, open(path_down, 'w') as down_out, open(path_comb, 'w') as comb_out:
		# TODO: Output basic metadata at top of file?
		for gene, pvalue in gene_pvalues:
			abs_score = abs(pvalue)
			if pvalue > 0:
				up_out.write('%s\t%f\n' % (gene, pvalue))
			else:
				down_out.write('%s\t%f\n' % (gene, abs_score))
			# This file is just for Enrichr, which doesn't accept negative
			# numbers for its levels of membership. A client wouldn't want a
			# combined file without signs.
			comb_out.write('%s\t%f\n' % (gene, abs_score))
	return flask.jsonify({
		'up': path_up,
		'down': path_down,
		'comb': path_comb,
		'conversion_pct': conversion_pct
	})
	'''


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