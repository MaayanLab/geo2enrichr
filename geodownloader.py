"""This module is responsible for downloading GEO SOFT files. SOFT file URLs
depend on whether the file type is GDS or GSE. This module abstracts that
conditional away.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Andrew Rouillard, Matthew Jones, Avi Ma'ayan"
__contact__ = "avi.maayan@mssm.edu"
"""


import gzip
import urllib2
import StringIO
import sys

import filemanager
from files import GEOFile


def download(accession, metadata):
	"""Downloads GEO file based on accession number. Returns a GEOFile
	instance with optional metadata as annotations.

	While `metadata` is optional, optional arguments are handled at the
	endpoints, meaning that `RequestParams` will set `metadata` to an empty
	dict if no metadata is provided.
	"""

	if 'GDS' in accession:
		url = __construct_GDS_url(accession)
	else:
		url = __construct_GSE_url(accession)
	print 'URL constructed: ' + url
	bin_string = __get_file_by_url(url)
	if bin_string is None:
		# TODO: Throw an error
		return 'Error: File does not exist.'
	try:
		string = __unzip(bin_string)
	except IOError:
		return 'Error: Cannot get file from GEO. Please try again later.'

	geofile = GEOFile(accession, metadata, 'soft')
	with open(geofile.full_path, 'w') as f:
		f.write(string)
	return geofile


def __get_file_by_url(url, attempts=5):
	"""Attempts to get the file from URL. Tries 5 times before giving up.
	"""

	while attempts > 0:
		try:
			response = urllib2.urlopen(url)
		except urllib2.URLError:
			print 'Failed to download'
			# TODO: Throw an error
			return None
		if response.getcode() < 201:
			break
		else:
			attempts -= 1
	else:
		return None

	return response.read()


def __unzip(compressed_string):
	"""Unzips the file without allowing it to touch the disk.
	"""

	f = StringIO.StringIO(compressed_string)
	decompressed = gzip.GzipFile(fileobj=f)
	print 'Unzipping file'
	return decompressed.read()


def __construct_GDS_url(accession):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/datasets/GDS4nnn/GDS4999/soft/GDS4999.soft.gz
	"""

	number_digits = len(accession) - 3  # "GDS" is of length 3.
	if number_digits > 3:
		folder = accession[:4] + "nnn"
	else:
		folder = accession[:3] + "n" * number_digits
	url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/datasets", 
		folder,
		accession,
		"soft",
		accession + ".soft.gz"])
	return url


def __construct_GSE_url(accession):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GSE4nnn/GSE4999/matrix/GSE4999.txt.gz
	"""

	number_digits = len(accession) - 3  # "GSE" is of length 3.
	if number_digits < 4:
		folder = accession[:3] + 'nnn'  # e.g. GSEnnn.
	elif 3 < number_digits < 5:
		folder = accession[:4] + 'nnn'  # e.g. GSE1nnn.
	else:
		folder = accession[:5] + 'nnn'  # e.g. GSE39nnn.
	url = '/'.join(['ftp://ftp.ncbi.nlm.nih.gov/geo/series', 
		folder,
		accession,
		'matrix',
		accession + '_series_matrix.txt.gz'])
	return url