"""This module handles all valid query string arguments to all API endpoints;
it sets all necessary default values, so functions further down the callstack
do not need to.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


from collections import namedtuple
Metadata = namedtuple('Metadata', 'platform organism cell perturbation gene disease')


class RequestArgs:


	def __init__(self, args):
		self.accession = args.get('accession') if 'accession' in args else None
		self.filename  = args.get('filename')  if 'filename'  in args else None
		
		self.up       = args.get('up')       if 'up'   in args else None
		self.down     = args.get('down')     if 'down' in args else None
		self.combined = args.get('combined') if 'up'   in args else None

		self.A_cols = [x.encode('ascii') for x in args.get('control').split('-')]      if 'control'      in args else None
		self.B_cols = [x.encode('ascii') for x in args.get('experimental').split('-')] if 'experimental' in args else None

		# Set the user's default options in case the client-side code does not.
		self.config = {
			'method' : args.get('method').encode('ascii') if args.get('method') else 'chdir',
			# TODO: Make this configurable by on the client.
			'cutoff' : 500
		}

		# We use a namedtuple to retain order yet legibility.
		# Order is important so we can stringify the tuple in a consistent
		# format.
		#
		# TODO: "platform" is *not* metadata. It is absolutely required for
		# this application to work properly. "platform" was added to the
		# "metadata" tuple to make adding it to the filename easier. This was
		# a mistake and should be undone when possible.
		platform       = args.get('platform').encode('ascii')     if 'platform'     in args else None
		organism       = args.get('organism').encode('ascii')     if 'organism'     in args else None
		cell           = args.get('cell').encode('ascii')         if 'cell'         in args else None
		perturbation   = args.get('perturbation').encode('ascii') if 'perturbation' in args else None
		gene           = args.get('gene').encode('ascii')         if 'gene'         in args else None
		disease        = args.get('disease').encode('ascii')      if 'disease'      in args else None
		self.metadata  = Metadata(platform, organism, cell, perturbation, gene, disease)
