"""This module has the API endpoints for GEO2Enrichr.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sys

import flask

from softfile import *
from genelist import *
from server import *
import database as db
from server.crossdomain import crossdomain


app = flask.Flask(__name__)
app.debug = True


# In production, Apache HTTPD handles serving static files.
if app.debug:
	# This forces the browser to download txt files rather than rendering
	# them. See http://stackoverflow.com/a/3749395/1830334.
	import mimetypes
	mimetypes.add_type('application/x-please-download-me', '.txt')


ALLOWED_ORIGINS = '*'
PATH = '/g2e'


@app.route(PATH, methods=['GET'])
@crossdomain(origin='*')
def index_endpoint():
	"""Returns verification that the server is running.
	"""
	return app.send_static_file('webapp.html')


@app.route(PATH + '/getgeo', methods=['PUT', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def getgeo_endpoint():
	"""Returns a JSON blob representing the GEO SOFT file. Takes an optional
	argument to indicate that the data should not be cleaned. Does not
	download the data from GEO if the file exists the server.
	"""
	args = GetGeoRequestArgs(flask.request.json)
	sf = SoftFile.from_geo(args.dataset, args.platform, args.A_cols, args.B_cols, args.norm)
	return get_flask_json_response(sf.__dict__)


@app.route(PATH + '/getcustom', methods=['PUT', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def custom_endpoint():
	"""
	"""
	args = CustomRequestArgs(flask.request)
	if args.example:
		sf = SoftFile.from_example()
	else:
		sf = SoftFile.from_file(args.name, args.file, args.platform)
	return get_flask_json_response(sf.__dict__)


@app.route(PATH + '/diffexp', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def diffexp_endpoint():
	"""Identifies differentially expressed genes for any input of genes and
	expression values.
	"""
	args = DiffExpRequestArgs(flask.request.json)
	gl = GeneList(args.A, args.B, args.genes, args.method, args.cutoff)
	return get_flask_json_response(gl.__dict__)















'''
@app.route(PATH + '/enrichr', methods=['GET', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def enrichr_endpoint():
	"""Parses files on the server, pipes the results to Enrichr, and returns a
	valid link.
	"""
	args = svr.RequestArgs(flask.request.json)
	up_link =  dp.enrichrlink.get_link(args.up, args.up.split('.')[0])
	# Do not use Enrichr if the first timeout fails. Assume Enrichr is down.
	down_link = dp.enrichrlink.get_link(args.down, args.down.split('.')[0]) if up_link else ''
	combined_link = dp.enrichrlink.get_link(args.combined, args.combined.split('.')[0]) if up_link else ''

	return flask.jsonify({
		'status': 'ok',
		'up': up_link,
		'down': down_link,
		'combined': combined_link
	})


@app.route(PATH + '/stringify', methods=['POST', 'OPTIONS'])
@crossdomain(origin=ALLOWED_ORIGINS, headers=['Content-Type'])
def stringify_endpoint():
	"""
	"""

	args = svr.RequestArgs(flask.request.json)
	up_genes = svr.GeneFile(args.up)
	dn_genes = svr.GeneFile(args.down)
	return flask.jsonify({
		'status': 'ok',
		'up': up_genes.to_str('-', False),
		'down': dn_genes.to_str('-', False)
	})


@app.route(PATH + '/count', methods=['GET'])
@crossdomain(origin=ALLOWED_ORIGINS)
def count_entpoint():
	"""Returns the number of gene lists that have been extracted from GEO.
	"""

	return flask.jsonify({
		'status': 'ok',
		'extraction_count': db.get_extraction_count()
	})


@app.route(PATH + '/diseases', methods=['GET'])
@crossdomain(origin=ALLOWED_ORIGINS)
def rare_diseases_endpoint():
	"""Returns a list of rare diseases.
	"""

	return flask.jsonify({
		'status': 'ok',
		'rare_diseases': db.get_rare_diseases()
	})


@app.route(PATH + '/platforms', methods=['GET'])
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
#	})'''



'''

# TODO: This is an absolutely awful hack that I (GWG) wrote to get the `full`
# endpoint restabilized for a user. Long term, we *must* re-architecture this
# module so that we are more dry.
#
# Nearly every line of code is actually repeated somewhere else in this
# module. Comments should be with the original code.
@app.route(PATH + '/full', methods=['GET'])
@crossdomain(origin='*')
def full_endpoint():

	s = time.time()

	args = svr.RequestArgs(flask.request.args)
	filename = dp.geodownloader.download(args.accession, args.metadata).filename

	A, B, genes, conversion_pct = dp.softparser.parse(filename, args.metadata.platform, args.A_cols, args.B_cols)
	A, B, genes = dp.cleaner.normalize(A, B, genes)

	gene_pvalue_pairs = dp.diffexper.analyze(A, B, genes, args.config, filename)
	output_files = svr.filewriter.output_gene_pvalue_pairs(filename, gene_pvalue_pairs)
	
	accession = filename.split('_')[0]
	db.euclid.record_extraction(accession, args.A_cols, args.B_cols, args.metadata, args.config)

	up   = output_files['up']
	down = output_files['down']

	response = {
		'status': 'ok',
		'time': time.time() - s,
		'conversion_pct': str(conversion_pct),
		'up_genes': svr.GeneFile(up).to_dict(include_membership=True),
		'down_genes': svr.GeneFile(down).to_dict(include_membership=True),
	}
	if args.config.cutoff:
		response['up_enrichr'] = dp.enrichrlink.get_link(up, up.split('.')[0])
		response['down_enrichr'] = dp.enrichrlink.get_link(down, down.split('.')[0])
	return flask.jsonify(response)'''




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
