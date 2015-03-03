"""Handles the Enrichr API.

__authors__ = "Gregory Gundersen, Edward Y Chen"
__contact__ = "avi.maayan@mssm.edu"
"""


#import cookielib
#import poster
#import socket
#import urllib2

import requests

#from server.log import pprint
#from server.files import GeneFile


BASE_URL = 'http://amp.pharm.mssm.edu/Enrichr/'



def get_link(genes, description):
	import pdb; pdb.set_trace()
	#genes_str = '\n'.join(genes[:25]).encode('ascii')
	genes_str = '\n'.join([t[0]+','+t[1] for t in genes]).encode('ascii')
	payload = {
		'list': genes_str,
		'description': ''
	}
	sess = requests.session()
	
	# 1. POST the data to the server. We do not need the response.
	sess.post(BASE_URL + 'enrich', files={ 'list': (None, genes_str), 'description': (None, 'this is a test') })
	
	# 2. GET our link via the "share" endpoint. The requests module (and
	# Enrichr) handle cookies for us.
	resp = sess.get(BASE_URL + 'share')
	link_id = resp.text.split('"')[3]
	return BASE_URL + 'enrich?dataset=' + link_id
