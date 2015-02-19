import os.path

from geodownloader import download
from parser import parse
from normalizer import normalize
from server.log import pprint


class SoftFile(object):

	def __init__(self, dataset, platform, gsms=None):
		self.dataset = dataset
		self.platform = platform
		self.gsms = gsms
		if not os.path.isfile(self.path()):
			# This function writes a file to disk; the file's location can be
			# found at self.path().
			download(self.dataset, self.path())
		self.expression_values, self.conversion_pct = parse(self.path(), self.platform, self.gsms)

	def path(self):
		return 'static/soft/' + self.dataset + '.soft'

	def normalize(self):
		ev = self.expression_values
		normalize(ev.keys(), ev.values())
