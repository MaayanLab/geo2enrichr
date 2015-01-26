"""Handles the L1000CDS API.

__authors__ = "Gregory Gundersen, Qiaonan Duan"
__contact__ = "avi.maayan@mssm.edu"
"""


import cookielib
import urllib
import urllib2
import poster

from files import GeneFile


BASE_URL = 'http://amp.pharm.mssm.edu/lssr/input'


def get_link(filename):
	gene_str = GeneFile(filename).stringify_contents()
	link = _post_and_build_link(gene_str)
	return link


def _post_and_build_link(genes_str):
	""" POST a gene list to Enrichr server and get a stable link to the
	enriched data.
	"""

	params = {
		'upGenes': ['a', 'b'],
		'dnGenes': ['c' ,'d']
	}

	data = urllib.urlencode(params)
	req = urllib2.Request(BASE_URL, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page
	import pdb
	pdb.set_trace()
	#split_phrases = response_str.split('"')
	#link_ID = split_phrases[3]
	#share_url_head = BASE_URL + 'enrich?dataset='
	#enrichr_link = share_url_head + link_ID
