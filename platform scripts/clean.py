import os


#http://www.ncbi.nlm.nih.gov/geo/browse/?view=platforms&tool=findplatform


# Directories
PATH       = os.path.dirname(os.path.realpath(__file__)) + '/'
CLEANED    = PATH + 'cleaned/'
DOWNLOADED = PATH + 'downloaded/'
PARSED     = PATH + 'parsed/'



# File symbols
BOF  = '!platform_table_begin'
EOF  = '!platform_table_end'


def clean_dl_files():
	for fn in os.listdir(DOWNLOADED):
		accession = fn.split('.')[0]
		filename = DOWNLOADED + fn

		cleaned_result = __clean_gpl_file(accession, filename)
		if not cleaned_result:
			os.remove(filename)
			print 'Removed: ' + accession
			continue
		else:
			print 'Cleaned: ' + accession


def __clean_gpl_file(accession, gpl_file):
	is_empty = False
	cleaned_file = CLEANED + accession + '.txt'
	with open(gpl_file, 'r') as inf, open(cleaned_file, 'w+') as outf:
		BOF_not_found = True
		for line in inf:
			line = line.strip()
			if line != BOF and BOF_not_found:
				continue
			else:
				if BOF_not_found:
					BOF_not_found = False
					# Also, skip the BOF line.
				elif line == EOF:
					return True
				else:
					outf.write(line + '\n')
	# If there is an EOF (there should be), this won't execute.
	#print 'Delete - there was no end of file for: ' + accession
	return False


if __name__ == '__main__':
	clean_dl_files()