import os
from builder import PROBE2GENE


LOG = 'log_concat.txt'


def concat():
	log = open(LOG, 'w')
	outfile = open('output.txt', 'w+')
	for filename in os.listdir(os.getcwd() + '/symbols'):
		accession = filename.split('.')[0]
		if filename == '.DS_Store':
			continue

		if accession in PROBE2GENE:
			log.write('Already exists ' + accession + '\n')
			continue

		with open('symbols/' + filename) as infile:
			for line in infile:
				outfile.write(line)



if __name__ == '__main__':
	f = open(LOG, 'w+')
	f.close()
	concat()
