# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import os
import re

import flask
#from flask import Flask
#from flask import request
from collections import namedtuple
import mimetypes

import geofetcher
import geoparser
import util


app = flask.Flask(__name__)
app.debug = True

# This forces the browser to download txt files rather than rendering them.
# http://stackoverflow.com/a/3749395/1830334
mimetypes.add_type('application/x-please-download-me', '.txt')


@app.route('/')
def index():
	return 'It works!'


@app.route('/refresh')
def refresh():
	return 'TODO! Clean out the directories'


@app.route('/dlgeo')
def dlgeo():
	"""Takes an an accession number and optional annotations and downloads the
	file from GEO.
	"""

	# TODO: Check if the file already exists on the file system.

	p = __get_params(flask.request)

	if 'GDS' in p.accession_num:
		downloaded_file = geofetcher.get_soft_file(p.accession_num, p.directory, p.annotations)
	else:
		downloaded_file = geofetcher.get_series_matrix_file(p.accession_num, p.platform, p.directory, p.annotations)
	return flask.jsonify(downloaded_file)


@app.route('/diffexp')
def diffexp():
	"""Analyzes an existing SOFT file on the server."""

	p = __get_params(flask.request)

	is_GDS = 'GDS' in p.filename 
	if is_GDS:
		control      = [x.upper() for x in p.control]
		experimental = [x.upper() for x in p.experimental]
	else:
		control      = ['"{}"'.format(x.upper()) for x in p.control]
		experimental = ['"{}"'.format(x.upper()) for x in p.experimental]

	#util.get_path_to_geo_files(p.directory, p.filename)
	full_path = p.directory + p.filename

	try:
		if is_GDS:
			response = geoparser.parse_soft(full_path, p.use_chdir, control_names=control, experimental_names=experimental)
		else:
			response = geoparser.parse_series_matrix(full_path, p.use_chdir, control_names=control, experimental_names=experimental)
		os.remove(full_path)
	except IOError:
		response = {
			'error': 'IOError',
			'message': 'Error reading GEO file from server'
		}

	return flask.jsonify(response)


@app.route('/enrichr')
def enrichr():
	"""Parses any files on the server and returns a valid Enrichr link
	"""

	files = flask.request.args.get('files').encode('ascii').split('-')
	links = []

	for f in files:
		gene_str = util.build_gene_str_from_tsv(f)
		link = util.get_enrichr_link(gene_str)
		links.append(link)
	
	return flask.jsonify({
		'links': links
	})


def __get_params(request):
	"""Builds a paramaters tuple from the incoming request.
	"""

	accession_num   = request.args.get('accession').encode('ascii') if request.args.get('accession')  else ''
	platform        = request.args.get('platform').encode('ascii') if request.args.get('platform') else ''
	control         = [x.encode('ascii') for x in request.args.get('control').split('-')] if request.args.get('control') else []
	experimental    = [x.encode('ascii') for x in request.args.get('experimental').split('-')]  if request.args.get('experimental')  else []
	method          = request.args.get('method').encode('ascii') if request.args.get('method') else ''
	species         = request.args.get('species').encode('ascii') if request.args.get('species') else ''
	
	use_chdir       = method == 'chdir'
	
	directory       = util.get_geo_directory(use_chdir)
	filename        = request.args.get('filename').encode('ascii') if request.args.get('filename') else ''

	# TODO: Make the annotations a hyphen-separated list of properties?
	if species and platform:
		annotations = species + '_' + platform
	elif species:
		annotations = species
	elif platform:
		annotations = platform
	else:
		annotations = ''
	
	# TODO Reduce the number of arguments.
	# Perlis: "If you have a procedure with 10 parameters, you probably missed some."
	Params = namedtuple('Params', 'accession_num filename directory platform species control experimental method annotations use_chdir')
	return Params(accession_num, filename, directory, platform, species, control, experimental, method, annotations, use_chdir)
















'''@app.route('/diffexporg')
def fulldiffexp():
	"""Example query:
		http://localhost:5000/diffexp?accessionnum=GDS2308&species=Musmusculus  &platform=GPL340            &control=GSM76330-GSM76329                  &experimental=GSM76332-GSM76333-GSM76334&method=True
		http://localhost:5000/diffexp?accessionnum=GDS2308&species=1_Musmusculus&platform=GPL340&tfname=AKT1&control=GSM76329-GSM76330-GSM76331-GSM76332&experimental=GSM76333-GSM76334-GSM76335-GSM76336
	"""

	has_querystring = len(request.args) > 0

	accession_num = species = platform = TF_name = control = experimental = method = inclusion = chdir = list_folder = ''

	if (has_querystring):

		# Get paramters from querystring
		accession_num		= request.args.get('accessionnum').encode('ascii')
		species				= request.args.get('species').encode('ascii')
		platform			= request.args.get('platform').encode('ascii')
		control				= [x.encode('ascii') for x in request.args.get('control').split('-')]
		experimental		= [x.encode('ascii') for x in request.args.get('experimental').split('-')]
		use_chdir			= request.args.get('method') == 'chdir'
		inclusion			= request.args.get('inclusion')
		chdir, list_folder	= util.get_directories(use_chdir)

		# Build files and get their names on the server.
		# These filenames should include their paths on the server.
		filenames = softmanager.process_request(accession_num, species, platform, TF_name, control, experimental, chdir, list_folder, use_chdir, False)

		if inclusion == 'up':
			gene_str = util.build_gene_str_from_tsv(filenames[0])
		elif inclusion == 'down':
			gene_str = util.build_gene_str_from_tsv(filenames[1])
		else:
			gene_str = util.build_gene_str_from_tsv(filenames[0]) + '\n' + util.build_gene_str_from_tsv(filenames[1])

		return util.get_enrichr_link(gene_str);

	# No querystring.
	else:
		result = 'differential expression endpoint'

	return result'''


if __name__ == '__main__':
	app.run()