"""This module handles all valid query string arguments to all API endpoints;
it sets all necessary default values, so functions further down the callstack
do not need to.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


from collections import namedtuple
Metadata = namedtuple('Metadata', 'platform organism cell perturbation')


class RequestParams:


	def __init__(self, args):
		self.accession = args.get('accession') if 'accession' in args else None
		self.filename  = args.get('filename')  if 'filename'  in args else None

		self.A_cols = [x.encode('ascii') for x in args.get('control').split('-')]      if 'control'      in args else None
		self.B_cols = [x.encode('ascii') for x in args.get('experimental').split('-')] if 'experimental' in args else None

		# Set the user's default options in case the client-side code does not.
		self.config = {
			'method'    : args.get('method').encode('ascii') if args.get('method') else 'chdir',
			'inclusion' : args.get('inclusion').encode('ascii') if args.get('inclusion') else 'up',
			# TODO: Make this configurable by on the client.
			'cutoff' : 500
		}

		# We use a namedtuple to retain order yet legibility.
		# Order is important so we can stringify the tuple in a consistent format.
		platform       = args.get('platform').encode('ascii')     if 'platform'     in args else None
		organism       = args.get('organism').encode('ascii')     if 'organism'     in args else None
		cell           = args.get('cell').encode('ascii')         if 'cell'         in args else None
		perturbation   = args.get('perturbation').encode('ascii') if 'perturbation' in args else None
		self.metadata  = Metadata(platform, organism, cell, perturbation)