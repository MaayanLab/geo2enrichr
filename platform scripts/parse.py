import os
import re


#http://www.ncbi.nlm.nih.gov/geo/browse/?view=platforms&tool=findplatform


# Directories
PATH    = os.path.dirname(os.path.realpath(__file__)) + '/'
CLEANED = PATH + 'cleaned/'
PARSED  = PATH + 'parsed/'


def parse_cleaned_files():
	for fn in os.listdir(CLEANED):
		accession = fn.split('.')[0]
		filename = CLEANED + fn
		parsed_result = __parse_cleaned_file(accession, filename)
		if not parsed_result:
			os.remove(filename)
			print 'Removed: ' + accession
			continue
		else:
			print 'Parsed : ' + accession


def __parse_cleaned_file(accession, clean_gpl_file):
	parsed_file = PARSED + accession + '.txt'
	header_parsed = False
	# Guard against a completely empty file being created.
	line_printed = False

	with open(clean_gpl_file, 'r') as inf, open(parsed_file, 'w+') as outf:
		for line in inf:

			# Find the column with gene symbols.
			if not header_parsed:
				header_parsed = True
				header = line.split('\t')
				
				probe_idx = __find_probe_index(header)
				gene_idx  = __find_gene_symbol_index(header)
				if probe_idx is None:
					#print 'Delete - cannot find probe column for: ' + accession
					return False
				if gene_idx is None:
					#print 'Delete - cannot find gene column for: ' + accession
					return False

			line = line.split('\t')
			try:
				if line[gene_idx] == '':
					#print 'Discard - no gene symbol.'
					continue

				probe = line[probe_idx].strip()
				gene  = line[gene_idx].strip()
				
				if probe == '':
					#print 'Discard - empty probe: ' + probe
					continue
				if '|' in probe:
					#print 'Discard - probe has pipe: ' + probe
					continue
				if gene == '':
					#print 'Discard - empty gene: ' + gene
					continue
				if '///' in gene or '|' in gene or ',' in gene:
					#print 'Discard - probe ID maps to multiple genes: ' + gene
					continue
				if '---' in gene:
					#print 'Discard - gene is invalid: ' + gene
					continue
			except IndexError:
				#print 'Error - line was an ' + str(type(line)) + ' rather than a string: ' + str(line)
				# Many platform files contain lines that do not have the same number of columns.
				continue

			outf.write(probe + '\t' + gene + '\n')
			line_printed = True
	if not line_printed:
		#print 'Delete - File was empty for: ' + accession
		return False
	else:
		return True


def __find_probe_index(header):
	if header[0] == 'ID':
		return 0
	for idx, word in enumerate(header):
		r = re.findall('ID', word)
		if r:
			return idx
	return None


def __find_gene_symbol_index(header):
	regexp = re.compile('genesymbol')
	for idx, word in enumerate(header):
		word = word.replace('_', '').replace(' ', '').lower()
		match = re.findall(regexp, word)
		if match:
			#print match[0]
			return idx
	regexp = re.compile('symbol')
	for idx, word in enumerate(header):
		word = word.replace('_', '').replace(' ', '').lower()
		match = re.findall(regexp, word)
		if match:
			#print match[0]
			return idx
	return None


if __name__ == '__main__':
	parse_cleaned_files()