# -----------------------------------------------------------------------------
# <credits, etc.>
#
# Flask automatically servers anything in the `static/` directory
# -----------------------------------------------------------------------------


from time import time


class GEOFile:

	GEO_FILES_DIR = 'static/geofiles/'


	def __init__(self, accession, metadata={}, extension='soft'):
		self.accession = accession
		self.annotations = filter(None, metadata)
		timestamp = ''#str(time())[:-3]

		if self.annotations:
			self.filename = self.accession + '_' + '-'.join(self.annotations) + '_' + timestamp + '.' + extension
		else:
			self.filename = self.accession + '_' + timestamp + '.' + extension

		self.full_path = GEOFile.GEO_FILES_DIR + self.filename


	@staticmethod
	def get_full_path(filename):
		return GEOFile.GEO_FILES_DIR + filename




class GeneFiles:

	GENE_FILES_BASE = 'static/genefiles/'


	def __init__(self, base_filename):
		GENE_FILE_EXTENSION = 'genes.txt'
		base_filename = base_filename.replace('.soft', '')
		
		self.up        = base_filename + '_up_'       + GENE_FILE_EXTENSION
		self.down      = base_filename + '_down_'     + GENE_FILE_EXTENSION
		self.combined  = base_filename + '_combined_' + GENE_FILE_EXTENSION
		self.directory = GeneFiles.GENE_FILES_BASE


	@staticmethod
	def get_full_path(filename):
		return GeneFiles.GENE_FILES_BASE + filename