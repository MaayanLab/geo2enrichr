"""This module handles all valid query string arguments to all API endpoints;
it sets all necessary default values, so functions further down the callstack
do not need to.

__authors__ = "Gregory Gundersen, Edward Y Chen"
__contact__ = "avi.maayan@mssm.edu"
"""


import cookielib
import urllib2
import poster

from files import GeneFile


def get_link(filename):
	gene_str = GeneFile(filename).stringify_contents()
	link = __post_and_build_link(gene_str)
	return link


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