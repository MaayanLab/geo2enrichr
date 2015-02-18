"""This module is responsible for downloading GEO SOFT files. SOFT file URLs
depend on whether the file type is GDS or GSE. This module abstracts that
conditional away.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Andrew Rouillard, Matthew Jones, Avi Ma'ayan"
__contact__ = "avi.maayan@mssm.edu"
"""


from gzip import GzipFile
import zlib
from urllib2 import urlopen, URLError
from StringIO import StringIO

from server.files import SOFTFile


def download(accession, metadata):
	"""Downloads GEO file based on accession number. Returns a SOFTFile
	instance with optional metadata as annotations.

	While `metadata` is optional, optional arguments are handled at the
	endpoints, meaning that `RequestParams` will set `metadata` to an empty
	dict if no metadata is provided.

	For reading and unzipping binary chunks, see:
		http://stackoverflow.com/a/27053335/1830334
		http://stackoverflow.com/a/2424549/1830334
	"""

	CHUNK_SIZE = 1024
	decompressor = zlib.decompressobj(16+zlib.MAX_WBITS)

	if 'GDS' in accession:
		url = _construct_GDS_url(accession)
	else:
		url = _construct_GSE_url(accession)
	response = _get_file_by_url(url)
	
	soft_file = SOFTFile(accession, metadata)
	with open(soft_file.path(), 'w+') as f:
		while True:
			bin_chunk = response.read(CHUNK_SIZE)
			if not bin_chunk:
				break
			string = decompressor.decompress(bin_chunk)
			f.write(string)
	return soft_file


def _get_file_by_url(url, attempts=5):
	"""Attempts to get the file from URL. Tries 5 times before giving up.
	"""

	while attempts > 0:
		try:
			response = urlopen(url)
		except URLError:
			raise IOError('urllib2 failed to open URL.')
		if response.getcode() < 201:
			break
		else:
			attempts -= 1
	else:
		raise IOError('urllib2 failed 5x to download the file.')
	return response


def _unzip(compressed_string):
	"""Unzips the file without allowing it to touch the disk.
	"""

	f = StringIO(compressed_string)
	decompressed = GzipFile(fileobj=f)
	print 'Unzipping file'
	return decompressed.read()


def _construct_GDS_url(accession):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/datasets/GDS4nnn/GDS4999/soft/GDS4999.soft.gz
	"""

	number_digits = len(accession) - 3  # 'GDS' is of length 3.
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


def _construct_GSE_url(accession):
	"""Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GSE4nnn/GSE4999/matrix/GSE4999.txt.gz
	"""

	number_digits = len(accession) - 3  # 'GSE' is of length 3.
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
