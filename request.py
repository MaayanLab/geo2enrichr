"""Handles all incoming requests to all API endpoints for the server.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


from collections import namedtuple

# We use a namedtuple to retain order, which is important for stringification,
# and legibility, i.e. tuple.prop rather than tuple[0].
Metadata = namedtuple('Metadata', 'platform organism cell perturbation gene disease')
Config = namedtuple('Config', 'method cutoff')


class RequestArgs:


	def __init__(self, args):
		"""Instantiate a RequestArgs instance, setting any necessary default values,
		so functions further down the callstack do not need to.
		"""

		self.accession = args.get('accession') if 'accession' in args else None
		
		self.A_cols = [x.encode('ascii') for x in args.get('control').split('-')]      if 'control'      in args else None
		self.B_cols = [x.encode('ascii') for x in args.get('experimental').split('-')] if 'experimental' in args else None	
		
		self.filename = args.get('filename')  if 'filename'  in args else None
		self.up       = args.get('up')       if 'up'   in args else None
		self.down     = args.get('down')     if 'down' in args else None
		self.combined = args.get('combined') if 'up'   in args else None

		self.targetApp = args.get('targetApp') if 'targetApp' in args else None

		# Set the user's default options in case the client-side code does not.
		# TODO: Make the cutoff configurable by on the client.
		method        = args.get('method').encode('ascii') if args.get('method') else 'chdir'
		self.config   = Config(method, 500)

		platform      = args.get('platform')  if 'platform'  in args else None
		organism      = args.get('organism').encode('ascii')     if 'organism'     in args else None
		cell          = args.get('cell').encode('ascii')         if 'cell'         in args else None
		perturbation  = args.get('perturbation').encode('ascii') if 'perturbation' in args else None
		gene          = args.get('gene').encode('ascii')         if 'gene'         in args else None
		disease       = args.get('disease').encode('ascii')      if 'disease'      in args else None
		self.metadata = Metadata(platform, organism, cell, perturbation, gene, disease)
