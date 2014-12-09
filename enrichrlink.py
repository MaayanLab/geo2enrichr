# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import cookielib
import urllib2
import poster

from files import GeneFiles


def get_link(filename):
	gene_str = __build_gene_str_from_tsv(filename)
	link = __post_and_build_link(gene_str)
	return {
		'link': link
	}


def __post_and_build_link(genes_str, cluster_info=''):
	""" POST a gene list to Enrichr server and get a stable link to the
	enriched data.
	"""

	BASE_URL = "http://amp.pharm.mssm.edu/Enrichr/"

	opener = poster.streaminghttp.register_openers()
	opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

	params = {
		'list': genes_str,
		'description': cluster_info
	}

	datagen, headers = poster.encode.multipart_encode(params)
	request = urllib2.Request(BASE_URL + 'enrich', datagen, headers)
	urllib2.urlopen(request)

	x = urllib2.urlopen(BASE_URL + 'share')
	response_str = x.read()
	split_phrases = response_str.split('"')
	link_ID = split_phrases[3]
	share_url_head = BASE_URL + 'enrich?dataset='
	enrichr_link = share_url_head + link_ID
	return enrichr_link


def __build_gene_str_from_tsv(tsv_file):
	"""Parse TSV file and return a string formatted for a POST request to
	Enrichr.
	"""

	full_path = GeneFiles.get_full_path(tsv_file)
	result = ''
	with open(full_path) as f:
		for i, line in enumerate(f):
			split_line = line.rstrip().split('\t')
			gene = split_line[0]
			membership = split_line[1]
			result += gene + ',' + membership + '\n'

	return result