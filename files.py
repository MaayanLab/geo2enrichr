"""This module contains two classes for abstracting files on the server.
Importantly, these classes know where they live on the server and can be
jsonified as a response. They also annotate and timestamp themselves.

Note that Flask automatically servers anything in the `static/` directory

__authors__ = "Gregory Gundersen"
__credits__ = "Axel Feldmann, Kevin Hu, Andrew Rouillard, Matthew Jones, Avi Ma'ayan"
__contact__ = "avi.maayan@mssm.edu"
"""


from time import time


class File(object):

	def __init__(self, filename, directory, extension, metadata=None):
		if metadata:
			self.annotations = filter(None, metadata)
			anno = '-'.join(self.annotations)
		else:
			anno = None
		timestamp = ''#str(time())[:-9]
		self.filename = '_'.join(filter(None, [filename, anno, timestamp])) + extension
		self.directory = directory

	# Does this need to be a method? What is the value?
	def path(self):
		return 'static/' + self.directory + self.filename




class SOFTFile(File):

	def __init__(self, accessionOrFile, metadata=None):
		# This constructor can take either an accession number or a reference
		# to a SOFT file on the server. In case of the latter, remove the file
		# extension.
		accessionOrFile = accessionOrFile.replace('.soft', '')
		super(SOFTFile, self).__init__(accessionOrFile, 'soft/', '.soft', metadata)




class GeneFile(File):

	def __init__(self, filename, suffix):
		super(GeneFile, self).__init__(filename, 'genes/', suffix+'.genes.txt')




class ParsedFile(File):

	def __init__(self, filename):
		super(ParsedFile, self).__init__(filename, 'parsed/', '.txt')