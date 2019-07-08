import os
from builder import PROBE2GENE


LOG = 'log_concat.txt'


def concat():
	log = open(LOG, 'w', encoding='utf-8')
	outfile = open('output.txt', 'w+', encoding='utf-8')
	for filename in os.listdir(os.getcwd() + '/symbols'):
		accession = filename.split('.')[0]
		if filename == '.DS_Store':
			continue

		if accession in PROBE2GENE:
			log.write('Already exists ' + accession + '\n')
			continue

		with open('symbols/' + filename, encoding='utf-8') as infile:
			for line in infile:
				outfile.write(line)



if __name__ == '__main__':
	f = open(LOG, 'w+', encoding='utf-8')
	f.close()
	concat()
