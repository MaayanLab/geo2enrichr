"""Handles the Enrichr API.

__authors__ = "Gregory Gundersen, Edward Y Chen"
__contact__ = "avi.maayan@mssm.edu"
"""


import cookielib
import poster
import socket
import urllib2

from server.log import pprint
from server.files import GeneFile


BASE_URL = 'http://amp.pharm.mssm.edu/Enrichr/'


def get_link(filename, description):
	"""Attempts to return a link to Enrichr. Returns the string 'None' if it
	fails.
	"""

	gene_str = GeneFile(filename).to_str()
	link = ''
	try:
		link = _post_and_build_link(gene_str, description)
	except socket.timeout:
		pprint('Error using Enrichr\'s API')
	return link


def _post_and_build_link(genes_str, description):
	""" POST a gene list to Enrichr server and get a stable link to the
	enriched data.
	"""

	opener = poster.streaminghttp.register_openers()
	opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

	params = {
		'list': genes_str,
		'description': description
	}

	datagen, headers = poster.encode.multipart_encode(params)
	request = urllib2.Request(BASE_URL + 'enrich', datagen, headers)
	urllib2.urlopen(request, timeout=20)

	x = urllib2.urlopen(BASE_URL + 'share')
	response_str = x.read()
	split_phrases = response_str.split('"')
	link_ID = split_phrases[3]
	share_url_head = BASE_URL + 'enrich?dataset='
	enrichr_link = share_url_head + link_ID
	return enrichr_link
