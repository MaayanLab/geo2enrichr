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


class CustomRequestArgs:

	def __init__(self, request):
		self.file = request.files['file']
		name = request.form.get('name') or self.file.name
		self.name = name
		self.platform = request.form.get('platform')
