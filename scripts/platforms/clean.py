import os
import sys


LOG = 'log_cleaner.txt'
BOF = '!platform_table_begin'


def clean(filename, idx=None):
	accession = filename.split('.')[0]
	try:
		with open('downloaded/' + filename, encoding='utf-8') as f, open('cleaned/' + filename, 'w+', encoding='utf-8') as cf, open(LOG, 'a', encoding='utf-8') as log:
			discard = next(f)
			while discard.rstrip() != BOF:
				discard = next(f)

			header = next(f).split('\t')
			length = len(header)
			header = [i.lower() for i in header]
			
			if not idx:
				try:
					gene_sy_i = header.index('gene symbol')
				except ValueError as e:
					log.write('error finding gene symbol column: ' + accession)
			else:
				gene_sy_i = idx

			probe_id_i = 0
			for l in f:
				line = l.split('\t')
				if len(line) != len(header):
					continue

				probe_id = line[probe_id_i]
				gene_sy = line[gene_sy_i]

				if probe_id == '' or gene_sy == '':
					continue
				if '|' in probe_id or '\\' in probe_id or '/' in probe_id:
					continue
				if '|' in gene_sy or '\\' in gene_sy or '/' in gene_sy:
					continue

				cf.write(accession + '\t' + probe_id + '\t' + gene_sy + '\n')
		print('Cleaned ' + accession)

	except Exception, e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		log = open(LOG, 'a', encoding='utf-8')
		log.write('Error ' + accession + ': ' + str(exc_type) + '\n')
		log.close()

		

if __name__ == '__main__':
	f = open(LOG, 'w+', encoding='utf-8')
	f.close()
	for filename in os.listdir(os.getcwd() + '/downloaded'):
		clean(filename)
