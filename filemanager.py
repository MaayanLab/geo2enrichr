# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import cookielib
import poster
import time
import urllib2

#from probe2gene import PROBE2GENE
from files import GeneFiles


def build_output_file(scores, use_chdir, base_filename):
	print "Now printing up and down gene lists..."
	print len(scores)

	unique_scores = dict()
	for symbol, score in scores:
		if symbol not in unique_scores or __passes_unique_score_threshold(use_chdir, score, unique_scores[symbol]):
			unique_scores[symbol] = score

	items = unique_scores.items()
	items.sort(key=lambda x: abs(x[1]), reverse=(True if use_chdir else False))

	#Convert Probe IDs to Gene Symbols
	if 'GSE' in base_filename:	
		print "Now converting probe IDs..."
		y = __convert_probe_IDs(items)
		items = y[0]
		print y[1]

	genefiles      = GeneFiles(base_filename)
	full_path_up   = genefiles.directory + genefiles.up
	full_path_down = genefiles.directory + genefiles.down
	full_path_comb = genefiles.directory + genefiles.combined

	with open(full_path_up, 'w') as up_out, open(full_path_down, 'w') as down_out, open(full_path_comb, 'w') as comb_out:
		for symbol, score in items:
			abs_score = abs(score)
			if score > 0:
				up_out.write('%s\t%f\n' % (symbol, score))
			else:
				down_out.write('%s\t%f\n' % (symbol, abs_score))
			# This file is just for Enrichr, which doesn't accept negative
			# numbers for its levels of membership. A client wouldn't want a
			# combined file without signs.
			comb_out.write('%s\t%f\n' % (symbol, abs_score))

	print "All done!"
	return genefiles.__dict__


def __convert_probe_IDs(list_to_convert):	
	#Step 2: Convert symbols in items
	print len(list_to_convert)
	converted_items = []
	unable_to_convert_list = []
	total_probe_ID = []
	for probe, pvalue in list_to_convert:
		if '"' in probe or "'" in probe:
			probe = probe[1:-1] #to strip quotes, assuming there are quotes

		if probe in PROBE2GENE:
			converted_items.append((PROBE2GENE[probe], pvalue))
		else:
			unable_to_convert_list.append(probe)
		total_probe_ID.append(probe)
	try:
		conversion_percent = float(len(converted_items))/float(len(total_probe_ID))
	except:
		conversion_percent = 0
	
	read_out = 'We tried to match {0} probes, but could only convert {1} of them, and could not convert {2}\
	of them. That is a success rate of {3}'.format(len(total_probe_ID), len(converted_items),\
	len(unable_to_convert_list), conversion_percent)

	return (converted_items, read_out)


def __passes_unique_score_threshold(use_chdir, score, unique_score):
	if use_chdir:
		return abs(score) > abs(unique_score)
	else:
		return abs(score) < abs(unique_score)


# We wish to identify which soft files we want
# Now obtain and parse each accession-associated SOFT file one-by-one
def __open_probe_dict(probe_dict):
	# Step 1: Get Conversion Dictionary
	with open(probe_dict) as f:
		probe_2_symbol_dict = {}
		for i, line in enumerate(f):
			split_line = line.rstrip().split('\t')
			probe = split_line[0]
			try:
				symbol = split_line[1]
				probe_2_symbol_dict[probe] = symbol
			except:
				continue
		return probe_2_symbol_dict


probe_2_symbol_dict = __open_probe_dict("Probe_2_Symbol_Unique.txt")