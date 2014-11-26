# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import cookielib
import urllib2
import poster
import time


# We wish to identify which soft files we want
# Now obtain and parse each accession-associated SOFT file one-by-one
def open_probe_dict(probe_dict):
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


def get_geo_directory(use_chdir):
	if use_chdir:
		return 'static/geofiles/chdir/'
	else:
		return 'static/geofiles/anova/'


def get_path_to_geo_files(directory, filename):
	# Use "static" so Flask will automatically server these files.
	return 'static/geofiles/' + directory + '/' + filename


def get_path_to_gene_files():
	# Use "static" so Flask will automatically server these files.
	return 'static/genefiles/'


def get_gene_filename(up_or_down, prefix=''):
	return str(time.time())[:-3] + '_' + prefix + '_' + up_or_down + '_genes.txt'


def output_into_file(scores, use_chdir, prefix=''):
	print "Now printing up and down gene lists..."
	print len(scores)

	unique_scores = dict()
	for symbol, score in scores:
		if symbol not in unique_scores or __passes_unique_score_threshold(use_chdir, score, unique_scores[symbol]):
			unique_scores[symbol] = score

	items = unique_scores.items()
	items.sort(key=lambda x: abs(x[1]), reverse=(True if use_chdir else False))

	#Convert Probe IDs to Gene Symbols
	if 'GSE' in prefix:	
		print "Now converting probe IDs..."
		y = __convert_probe_IDs(items, probe_2_symbol_dict)
		items = y[0]
		print y[1]

	if prefix:
		prefix = prefix.split('/')[1]

	filename_up    = get_gene_filename('up',   prefix)
	filename_down  = get_gene_filename('down', prefix)
	directory      = get_path_to_gene_files()

	full_path_up   = directory + '/' + filename_up
	full_path_down = directory + '/' + filename_down

	with open(full_path_up, 'w') as up_out, open(full_path_down, 'w') as down_out:
		for symbol, score in items:
			if score > 0:
				up_out.write('%s\t%f\n' % (symbol, score))
			else:
				down_out.write('%s\t%f\n' % (symbol, abs(score)))
	print "All done!"
	#return #(filename_up, filename_down, directory)
	return {
		'up': filename_up,
		'down': filename_down,
		'directory': directory
	}


def __convert_probe_IDs(list_to_convert, probe_2_symbol_dict):	
	#Step 2: Convert symbols in items
	print len(list_to_convert)
	converted_items = []
	unable_to_convert_list = []
	total_probe_ID = []
	for probe, pvalue in list_to_convert:
		if '"' in probe or "'" in probe:
			probe = probe[1:-1] #to strip quotes, assuming there are quotes

		if probe in probe_2_symbol_dict:
			converted_items.append((probe_2_symbol_dict[probe], pvalue))
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


def get_enrichr_link(genes_str, cluster_info=''):
	""" POST a gene list to Enrichr server and get a stable link to the
	enriched data.
	"""

	opener = poster.streaminghttp.register_openers()
	opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

	params = {
		'list': genes_str,
		'description': cluster_info
	}

	datagen, headers = poster.encode.multipart_encode(params)
	BASE_URL = "http://amp.pharm.mssm.edu/Enrichr/"
	request = urllib2.Request(BASE_URL + 'enrich', datagen, headers)
	urllib2.urlopen(request)

	x = urllib2.urlopen(BASE_URL + 'share')
	response_str = x.read()
	split_phrases = response_str.split('"')
	link_ID = split_phrases[3]
	share_url_head = BASE_URL + 'enrich?dataset='
	enrichr_link = share_url_head + link_ID
	return enrichr_link


def build_gene_str_from_tsv(tsv_filename):
	"""Parse TSV file and return a string formatted for a POST request to
	Enrichr.
	"""

	full_path = get_path_to_gene_files() + tsv_filename

	result = ''
	with open(full_path) as f:
		for i, line in enumerate(f):
			split_line = line.rstrip().split('\t')
			gene = split_line[0]
			membership = split_line[1]
			result += gene + ',' + membership + '\n'
	print result
	return result


probe_2_symbol_dict = open_probe_dict("Probe_2_Symbol_Unique.txt")