import csv
import gzip
import os
from StringIO import StringIO
import urllib2


#http://www.ncbi.nlm.nih.gov/geo/browse/?view=platforms&tool=findplatform


# Directories
PATH       = os.path.dirname(os.path.realpath(__file__)) + '/'
INPUT      = PATH + 'input/'
DOWNLOADED = PATH + 'downloaded/'


def download_files_in(filename):
	# Open one homo sapiens file and one mus musculus file and
	# extract every GEO platform for these two species.
	with open(INPUT + filename) as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		# Consume header line.
		next(tsvin)
		for row in tsvin:
			accession = row[0]

			download_result = __download_gpl_file(accession)
			if not download_result[0]:
				os.remove(download_result[1])
				print 'Deleted   : ' + accession
				continue
			else:
				print 'Downloaded: ' + accession

	msg = 'All files downloaded'
	print len(msg)*'-'
	print msg


def __download_gpl_file(accession):
	#pdb.set_trace()
	bin_string = __get_gpl_as_response(accession)
	#pdb.set_trace()
	if bin_string is None:
		return (False, None, 'Error - cannot get file from GEO: ' + accession)
	try:
		string = __unzip(bin_string)
	except IOError:
		return (False, None, 'Error - could not unzip GEO file: ' + accession)

	if string:
		filename = DOWNLOADED + accession + '.txt'
		with open(filename, 'w+') as f:
			f.write(string)
		return (True, filename)
	return (False, None, 'Empty file:\t' + accession)


def __get_gpl_as_response(accession):
	"""Attempts to get the file from URL. Tries five times before giving up.
	"""
	
	urls = __construct_gpl_url(accession)
	return __open_url(urls[1])


def __open_url(url, attempts=5):
	response = None
	while attempts > 0:
		try:
			response = urllib2.urlopen(url)
			if response and response.getcode() < 201:
				break
			else:
				attempts -= 1
		except urllib2.URLError:
			print 'URLError with: ' + url
	return response.read()


def __construct_gpl_url(accession):
	'''Example URL:
		ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL4nnn/GDS4999/annot/GPL4999.annot.gz
		ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL15nnn/GPL15905/soft/GPL15905_family.soft.gz
	'''

	BASE  = 'ftp://ftp.ncbi.nlm.nih.gov/geo/platforms'
	ANNOT = 'annot'
	SOFT  = 'soft'
	GZ    = '.gz'

	# Remove 'GPL'
	number_digits = len(accession) - 3

	if number_digits < 4:
		folder = accession[:3] + 'nnn'
	elif 3 < number_digits < 5 :
		folder = accession[:4] + 'nnn'
	else:
		folder = accession[:5] + 'nnn'

	file_annot = accession + '.' + ANNOT + GZ
	file_soft  = accession + '_family.' + SOFT + GZ

	url_annot  = [BASE, folder, accession, ANNOT, file_annot]
	url_soft   = [BASE, folder, accession, SOFT,  file_soft]
	
	#return 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?form=text&acc=' + accession
	return ('/'.join(url_annot), '/'.join(url_soft))


def __unzip(bin_string):
	"""Unzips file without allowing it to touch the disk.
	"""

	f = StringIO(bin_string)
	decompressed = gzip.GzipFile(fileobj=f)
	return decompressed.read()


if __name__ == '__main__':
	download_files_in('homo sapiens.tsv')