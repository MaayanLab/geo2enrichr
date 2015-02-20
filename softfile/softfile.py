import os.path

from server.log import pprint
from geodownloader import download
from parser import parse
from normalizer import normalize


class SoftFile(object):

	def __init__(self, dataset, platform, A_cols, B_cols, norm=True):
		self.dataset = dataset
		self.platform = platform
		self.gsms = A_cols + B_cols
			
		if not os.path.isfile(self.path()):
			# This function writes a file to disk; the file's location can be
			# found at self.path().
			download(self.dataset, self.path())
		self.genes, self.A, self.B, self.stats = parse(self.path(), self.platform, A_cols, B_cols)
		# Convert to dictionary for easy normalizing and writing to file.
		AB = [x+y for x,y in zip(self.A, self.B)]
		gene_values_dict = { k:v for k,v in zip(self.genes, AB) }
		if norm:
			gene_values_dict = normalize(gene_values_dict)

		if not os.path.isfile(self.clean_path()):
			self._write(gene_values_dict)
		self.link = self.clean_path()

	def path(self):
		return 'static/soft/' + self.dataset + '.soft'

	def clean_path(self):
		return 'static/soft/clean/' + self.dataset + '-'.join(self.gsms) + '.soft'

	def _write(self, gene_values_dict):
		pprint('Writing clean SOFT file.')
		with open(self.clean_path(), 'w+') as f:
			f.write('!datset\t' + self.dataset + '\n')
			f.write('!platform\t' + self.platform + '\n')
			f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
			f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
			f.write('!end_metadata\n')
			f.write('GENE SYMBOL\t' + '\t'.join(self.gsms) + '\n')
			for gene, val in gene_values_dict.items():
				val_str = '\t'.join(map(str, val))
				f.write(gene + '\t' + val_str + '\n')
