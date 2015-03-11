"""This module creates an Extraction instance.
"""


class Extraction(object):

	def __init__(self, softfile=None, genelist=None):
		self.softfile = softfile
		self.genelist = genelist

	@classmethod
	def create(cls, softfile=None, genelist=None):
		return cls(softfile, genelist)
