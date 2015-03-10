"""Represents a single gene list-from-SOFT file extraction event.
"""


class Extraction(object):
	
	def __init__(self, softfile, genelist):
		self.softfile_id = softfile.id
		self.genelist_id = genelist.id

	@classmethod
	def create(cls, softfile, genelist):
		return cls(softfile, genelist)
