# -----------------------------------------------------------------------------
# <credits, etc.>
#
# Flask automatically servers anything in the `static/` directory
# -----------------------------------------------------------------------------


from time import time


class GEOFile:


	def __init__(self, accession, method, metadata={}, extension='soft'):
		self.accession = accession
		self.directory = self.get_directory(method)
		self.annotations = filter(None, metadata)
		timestamp = str(time())[:-3]

		if self.annotations:
			self.filename = self.accession + '_' + '-'.join(self.annotations) + '_' + timestamp + '.' + extension
		else:
			self.filename = self.accession + '_' + timestamp + '.' + extension

		self.full_path = self.directory + self.filename


	@staticmethod
	def get_directory(method, filename=None):
		GEO_FILES_BASE = 'static/geofiles/'
		directory = GEO_FILES_BASE + 'chdir/' if method == 'chdir' else GEO_FILES_BASE + 'anova/'
		if filename:
			return directory + filename
		return directory




class GeneFiles:


	def __init__(self, base_filename):
		GENE_FILE_EXTENSION = 'genes.txt'
		base_filename = base_filename.replace('.soft', '')
		
		self.up        = base_filename + '_up_'       + GENE_FILE_EXTENSION
		self.down      = base_filename + '_down_'     + GENE_FILE_EXTENSION
		self.combined  = base_filename + '_combined_' + GENE_FILE_EXTENSION
		self.directory = self.get_directory()


	@staticmethod
	def get_directory(filename=None):
		directory = 'static/genefiles/'
		if filename:
			return directory + filename
		return directory