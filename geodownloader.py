# -----------------------------------------------------------------------------
# <credits, etc.>
#
# Library for getting and processing GDS SOFT Files from GEO. GDS Files have a
# particular structure for the construction of their gzipped files. This script
# will take a GDS as input and return the samples (GSMs) and their experimental
# conditions with it
# -----------------------------------------------------------------------------


import gzip
import urllib2
import StringIO
import sys

import filemanager
from files import GEOFile


def download_geo_file(accession, options, metadata={}):
	if 'GDS' in accession:
		return __get_soft_file(accession, options, metadata)
	else:
		return __get_series_matrix_file(accession, options, metadata)


# `metadata` is a user-supplied argument for adding descriptors to the filename.
def __get_soft_file(accession, user_options, metadata):
	url = __construct_GDS_url(accession)
	bin_string = __get_file_by_url(url)

	if bin_string is None:
		return "Error: File does not exist."
	try:
		string = __unzip(bin_string)
	except IOError:
		return "Error: Cannot get file from GEO. Please try again later."

	geofile = GEOFile(accession, user_options['method'], metadata, 'soft')
	with open(geofile.full_path, 'w') as f:
		f.write(string)

	return geofile.__dict__


def __get_series_matrix_file(dataset_identifier, user_options, metadata):
	platform = metadata['platform']
	url = __construct_GSE_url(dataset_identifier, platform)
	bin_string = __get_file_by_url(url)

	if bin_string is None:
		return "Error: File does not exist."
	try:
		string = __unzip(bin_string)
	except IOError:
		return "Error: Cannot get file from GEO. Please try again later."

	geofile = GEOFile(accession, user_options['method'], metadata, 'txt')
	with open(geofile.full_path, 'w') as f:
		f.write(string)

	return geofile.__dict__


def __get_file_by_url(url, attempts=5):
	"""Attempts to get the file from URL. Tries five times before giving up.
	"""

	while attempts > 0:
		try:
			response = urllib2.urlopen(url)
		except urllib2.URLError:
			print url 
			sys.exit("Error: URL does not exist.")
		
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


def __construct_GDS_url(dataset_identifier):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/datasets/GDS4nnn/GDS4999/soft/GDS4999.soft.gz
	"""

	number_digits = len(dataset_identifier) - 3;    ## "GDS" is of length 3

	if number_digits > 3:
		folder = dataset_identifier[:4] + "nnn"
	else:
		folder = dataset_identifier[:3] + "n" * number_digits

	url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/datasets", 
									   folder,
									   dataset_identifier,
									   "soft",
									   dataset_identifier + ".soft.gz"])
	print 'URL constructed: ' + url
	return url


def __construct_GSE_url(dataset_identifier, platform):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GSE4nnn/GSE4999/matrix/GSE4999.txt.gz
	"""

	number_digits = len(dataset_identifier) - 3;    ## "GSE" is of length 3

	if number_digits < 4:
		folder = dataset_identifier[:3] + "nnn" #GSEnnn
	elif 3 < number_digits < 5:
		folder = dataset_identifier[:4] + "nnn" #GSE1nnn
	else:
		folder = dataset_identifier[:5] + "nnn" #GSE39nnn

	url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/series", 
										folder,
										dataset_identifier,
										"matrix",
										dataset_identifier + "_series_matrix.txt.gz"])
	print 'URL constructed: ' + url
	return url