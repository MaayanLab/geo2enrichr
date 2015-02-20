"""Handles all incoming requests to all API endpoints for the server.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


class GetGeoRequestArgs:

	def __init__(self, args):
		self.dataset = args.get('dataset')
		self.platform = args.get('platform')
		self.A_cols = args.get('A_cols')
		self.B_cols = args.get('B_cols')

		# Use "norm" instead of "normalize" for namespace reasons.
		if 'normalize' in args and args.get('normalize') is 'False':
			self.norm = False
		else:
			self.norm = True


class DiffExpRequestArgs:

	def __init__(self, args):
		self.genes = args.get('genes')
		self.A = args.get('A')
		self.B = args.get('B')
		if 'cutoff' in args:
			if args.get('cutoff') == 'None':
				self.cutoff = False
			else:
				self.cutoff = int(args.get('cutoff').encode('ascii'))
		else:
			# TODO: Change to 500 before deploying.
			self.cutoff = 200
		self.method = args.get('method') or 'chdir'


'''
class RequestArgs:

	def __init__(self, args):
		"""Instantiate a RequestArgs instance, setting any necessary default values,
		so functions further down the callstack do not need to.
		"""

		self.accession = args.get('accession') if 'accession' in args else None
		self.A_cols    = [x.encode('ascii') for x in args.get('control').split('-')]      if 'control'      in args else None
		self.B_cols    = [x.encode('ascii') for x in args.get('experimental').split('-')] if 'experimental' in args else None
		self.filename  = args.get('filename') if 'filename'  in args else None
		self.up        = args.get('up')       if 'up'   in args else None
		self.down      = args.get('down')     if 'down' in args else None
		self.combined  = args.get('combined') if 'up'   in args else None
		self.targetApp = args.get('targetApp') if 'targetApp' in args else None

		# Set the user's default options in case the client-side code does not.
		# TODO: Make the cutoff configurable by on the client.
		method  = args.get('method').encode('ascii') if 'method' in args else 'chdir'
		# Do *not* use bool() built-in:
		# http://stackoverflow.com/a/715455/1830334.
		absval  = args.get('absval').encode('ascii') == 'True' if 'absval' in args else True
		enrichr = args.get('enrichr').encode('ascii') == 'True' if 'enrichr' in args else True
		if 'cutoff' in args:
			cutoff = None if args.get('cutoff') == 'None' else int(args.get('cutoff').encode('ascii')) 
		else:
			cutoff = 500
		self.config = Config(absval, cutoff, enrichr, method)
		
		platform       = args.get('platform').encode('ascii') or None
		organism       = args.get('organism').encode('ascii') or None
		cell           = args.get('cell').encode('ascii') or None
		perturbation   = args.get('perturbation').encode('ascii') or None
		gene           = args.get('gene').encode('ascii') or None
		disease        = args.get('disease').encode('ascii') or None
		self.metadata  = Metadata(platform, organism, cell, perturbation, gene, disease)
'''
