"""Handles all incoming requests to all API endpoints for the server.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


import time


class GetGeoRequestArgs:

	def __init__(self, args):
		self.dataset = args.get('dataset')
		self.platform = args.get('platform')
		self.A_cols = args.get('A_cols')
		self.B_cols = args.get('B_cols')
		#self.method = args.get('method') or 'chdir'
		#self.cutoff = args.get('cutoff') or 500
		self.norm = args.get('norm') != 'False'


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
		self.enrichr = True if not args.get('enrichr') else False
		self.method = args.get('method') or 'chdir'
		self.cutoff = int(args.get('cutoff')) if args.get('cutoff') else 500
		self.norm = args.get('norm') != 'False'


class CustomRequestArgs:

	def __init__(self, request):
		if request.files:
			import pdb; pdb.set_trace()
			self.file = request.files['file']
			name = request.form.get('name') or self.file.filename
			self.name = name
			self.platform = request.form.get('platform')
			self.example = False
		else:
			self.example = True
