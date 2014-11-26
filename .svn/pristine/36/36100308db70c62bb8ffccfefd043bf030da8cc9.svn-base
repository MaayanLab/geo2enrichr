import chdir2
from scipy import stats
from collections import Counter
from math import log
import numpy

def open_probe_dict(probe_dict):
        #Step 1: Get Conversion Dictionary
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

def parse_series_matrix(filename, probe_2_symbol_dict, use_chdir=False, getFuzzy = False, control_indices=None, experimental_indices=None, control_names=None, experimental_names=None):
	# make list to store pvalues in later
	pvalues = []

	# chdir variables
	gene_order = []
	control = []
	experimental = []

	# removed probes
	rmvd_probes = []


	with open(filename) as series_matrix_file:
		# skip comments
		test = next(series_matrix_file)
		while test.rstrip() != '!series_matrix_table_begin':
			test = next(series_matrix_file)
		
		# read header
		header = next(series_matrix_file)
		header = header.rstrip('\r\n').split('\t')
		header = header[1:] #it is 2 in GDS Softs, but 1 in Series Matrix Files
		print header

		# find the columns indices
		if control_indices is None and experimental_indices is None:			
			control_indices = [header.index(gsm) for gsm in control_names]
			experimental_indices = [header.index(gsm) for gsm in experimental_names]
		counter = 0
		# read rest of series matrix
		for line in series_matrix_file:
			counter += 1
			if counter % 1000 == 0:
				print counter
			split_line = line.rstrip('\r\n').split('\t')
			if split_line[0] == '!series_matrix_table_end' or split_line[1] == '--Control':
				continue

			symbol = split_line[0] #it is 1 in GDS Softs, but 0 in Series Matrix Files
			values = split_line[1:] #it is 2 in GDS Softs, but 1 in Series Matrix Files

			if 'null' in values:
				##print 'removing line {0} with values {1}'.format(symbol, values)
				rmvd_probes.append((symbol, values))
				continue
			
			try:
				control_values = [float(values[i]) for i in control_indices]
				experimental_values = [float(values[i]) for i in experimental_indices]
			except ValueError:
				continue
			# perform ttest
			ttest_results = stats.ttest_ind(experimental_values, control_values)
			signed_pvalue = ttest_results[1] if ttest_results[0] > 0 else ttest_results[1]*-1
			pvalues.append((symbol, signed_pvalue))

			# fill in the chdir variables
			if use_chdir:
				gene_order.append(symbol)
				control.append(control_values)
				experimental.append(experimental_values)

	# sort pvalues
	print "now sorting pvalues..."
	print len(pvalues)
	pvalues.sort(key=lambda x: abs(x[1]))
	
	#multiple hypothesis correction
	corrected = False

	# try Bonferroni
	corrected_pvalues = [(x[0], x[1]*len(pvalues)) for x in pvalues if abs(x[1])*len(pvalues) < 0.05]
	if len(corrected_pvalues) > 100:
		corrected = True
		print 'Bonferroni correction with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.txt', ''), getFuzzy)
			return

	# try Benjamini-Hochberg
	if not corrected:
		previous_value = 1
		corrected_pvalues = []
		for i in range(len(pvalues), 0, -1):
			corrected_pvalue = min(abs(pvalues[i-1][1]) * len(pvalues) / i,previous_value)
			previous_value = corrected_pvalue
			corrected_pvalue = corrected_pvalue if pvalues[i-1] > 0 else -1*corrected_pvalue
			corrected_pvalues.append((pvalues[i-1][0], corrected_pvalue))
		corrected_pvalues = [x for x in corrected_pvalues if abs(x[1]) < 0.05]
		if len(corrected_pvalues) > 100:
			corrected = True
			print 'Benjamini-Hochberg correction with 0.05 cutoff'
			if use_chdir:
				down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
				up_threshold = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
				print threshold
			else:
				print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.txt', ''), getFuzzy)
				return

	# try uncorrected 0.01
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.01]
		if len(corrected_pvalues) > 100:
			print 'Uncorrected with 0.01 cutoff'
			corrected = True
			if use_chdir:
				down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
				up_threshold = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
				print threshold
			else:
				print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.txt', ''), getFuzzy)
				return

	# try uncorrected 0.05
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.05]
		print 'Uncorrected with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
			print threshold
		else:
			print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.txt', ''), getFuzzy)

	#call chdir if requested
	if use_chdir:
		print 'trying'
		chdir_scores = chdir2.chdir(gene_order, control, experimental, threshold)
		print 'success'
					
		print len(chdir_scores)
		unique_scores = dict()
		for symbol, score in chdir_scores:
			if symbol not in unique_scores or abs(score) > abs(unique_scores[symbol]):
				unique_scores[symbol] = score

		items = unique_scores.items()
		items.sort(key=lambda x: abs(x[1]), reverse=True)
		print "any scores"
		print len(items)

		#remove extension from filename
		if '.txt' in filename:
			filename = filename.replace('.txt', '')
		else:
			filename = filename.replace('.soft', '')

		suffix = filename[12:]

		if 'GSE' in suffix:	
			print "Now converting probe IDs..."
			y = probeID_convert(items, probe_2_symbol_dict)
			items = y[0]
			print y[1]

		subfold = 'ChDir_Lists/'
		
		with open(subfold + suffix + '_chdir_up_genes.txt', 'w') as up_out, open(subfold + suffix + '_chdir_down_genes.txt', 'w') as down_out:
			print subfold + suffix
			for symbol, score in items:
				if score > 0:
					up_out.write('%s\t%f\n' % (symbol, score))
				else:
					down_out.write('%s\t%f\n' % (symbol, abs(score)))
		return

	
def parse_soft(filename, probe_2_symbol_dict, use_chdir=False, getFuzzy=False, control_indices=None, experimental_indices=None, control_names=None, experimental_names=None):
	pvalues = []

	# chdir variables
	gene_order = []
	control = []
	experimental = []

	#removed probes
	rmvd_probes = []

	with open(filename) as soft_file:
		# skip comments
		test = next(soft_file)
		while test.rstrip() != '!dataset_table_begin':
			test = next(soft_file)
		
		# read header
		header = next(soft_file)
		header = header.rstrip('\r\n').split('\t')
		header = header[2:]
		print header

		# find the columns indices
		if control_indices is None and experimental_indices is None:			
			control_indices = [header.index(gsm) for gsm in control_names]
			experimental_indices = [header.index(gsm) for gsm in experimental_names]
		counter = 0
		# read rest of soft
		for line in soft_file:
			counter += 1
			if counter % 1000 == 0:
				print counter
			split_line = line.rstrip('\r\n').split('\t')
			if split_line[0] == '!dataset_table_end' or split_line[1] == '--Control':
				continue

			symbol = split_line[1]
			values = split_line[2:]

			if 'null' in values:
				##print 'removing line {0} with values {1}'.format(symbol, values)
				rmvd_probes.append((symbol, values))
				continue

			try:
				control_values = [float(values[i]) for i in control_indices]
				experimental_values = [float(values[i]) for i in experimental_indices]
			except ValueError:
				continue


			# always perform ttest
			ttest_results = stats.ttest_ind(experimental_values, control_values)
			signed_pvalue = ttest_results[1] if ttest_results[0] > 0 else ttest_results[1]*-1
			pvalues.append((symbol, signed_pvalue))

			if use_chdir:
				gene_order.append(symbol)
				control.append(control_values)
				experimental.append(experimental_values)

	# sort pvalues
	print "Now sorting pvalues..."
	pvalues.sort(key=lambda x: abs(x[1])) #gets rid of the sign, while sorting tuples by the pvalue
	print len(pvalues)

	#multiple hypothesis correction
	corrected = False

	# try Bonferroni
	corrected_pvalues = [(x[0], x[1]*len(pvalues)) for x in pvalues if abs(x[1])*len(pvalues) < 0.05]
	if len(corrected_pvalues) > 100:
		corrected = True
		print 'Bonferroni correction with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.soft', ''), getFuzzy)
			return

	# try Benjamini-Hochberg
	if not corrected:
		previous_value = 1
		corrected_pvalues = []
		for i in range(len(pvalues), 0, -1):
			corrected_pvalue = min(abs(pvalues[i-1][1]) * len(pvalues) / i,previous_value)
			previous_value = corrected_pvalue
			corrected_pvalue = corrected_pvalue if pvalues[i-1] > 0 else -1*corrected_pvalue
			corrected_pvalues.append((pvalues[i-1][0], corrected_pvalue))
		corrected_pvalues = [x for x in corrected_pvalues if abs(x[1]) < 0.05]
		if len(corrected_pvalues) > 100:
			corrected = True
			print 'Benjamini-Hochberg correction with 0.05 cutoff'
			if use_chdir:
				down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
				up_threshold = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
			else:
				print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.soft', ''), getFuzzy)
				return

	# try uncorrected 0.01
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.01]
		if len(corrected_pvalues) > 100:
			corrected = True
			print 'Uncorrected with 0.01 cutoff'
			if use_chdir:
				down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
				up_threshold = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
			else:
				print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.soft', ''), getFuzzy)
				return

	# try uncorrected 0.05
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.05]
		print 'Uncorrected with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			print_lists(corrected_pvalues, use_chdir, probe_2_symbol_dict, filename.replace('.soft', ''), getFuzzy)				

	if use_chdir:
		chdir_scores = chdir2.chdir(gene_order, control, experimental, threshold)
		print len(chdir_scores)
		unique_scores = dict()
		for symbol, score in chdir_scores:
			if symbol not in unique_scores or abs(score) > abs(unique_scores[symbol]):
				unique_scores[symbol] = score

		items = unique_scores.items()
		items.sort(key=lambda x: abs(x[1]), reverse=True)
		print "any scores?"
		print len(items)

		#remove extension from filename
		if '.txt' in filename:
			filename = filename.replace('.txt', '')
		else:
			filename = filename.replace('.soft', '')

		suffix = filename[12:]

		if 'GSE' in suffix:	
			print "Now converting probe IDs..."
			y = probeID_convert(items, probe_2_symbol_dict)
			items = y[0]
			print y[1]

		subfold = 'ChDir_Lists/'
		
		with open(subfold + suffix + '_chdir_up_genes.txt', 'w') as up_out, open(subfold + suffix + '_chdir_down_genes.txt', 'w') as down_out:
			print subfold + suffix
			for symbol, score in items:
				if score > 0:
					up_out.write('%s\t%f\n' % (symbol, score))
				else:
					down_out.write('%s\t%f\n' % (symbol, abs(score)))
		return

def probeID_convert(list_to_convert, probe_2_symbol_dict):	
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

def print_lists(pvalues, use_chdir, probe_2_symbol_dict, suffix='', getFuzzy = False):
	print "Now printing up and down gene lists..."
	print len(pvalues)
	unique_pvalues = dict()
	for symbol, pvalue in pvalues:
		if symbol not in unique_pvalues or abs(pvalue) < abs(unique_pvalues[symbol]):
			unique_pvalues[symbol] = pvalue

	items = unique_pvalues.items()
	items.sort(key=lambda x: abs(x[1]))

	#Convert Probe IDs to Gene Symbols
	if 'GSE' in suffix:	
		print "Now converting probe IDs..."
		y = probeID_convert(items, probe_2_symbol_dict)
		items = y[0]
		print y[1]

	if suffix:
		suffix = suffix[6:]

	#subfold = ''
	subfold = 'ANOVA/'
	with open(subfold + suffix + '_up_genes.txt', 'w') as up_out,\
	open(subfold + suffix + '_down_genes.txt', 'w') as down_out:
		symbols_list = []
		up_symbols = []
		down_symbols = []
		for symbol, pvalue in items:
			symbols_list.append(symbol)
			if pvalue > 0:
				up_out.write('%s\t%f\n' % (symbol, pvalue))
				up_symbols.append(symbol)
			else:
				down_out.write('%s\t%f\n' % (symbol, abs(pvalue)))
				down_symbols.append(symbol)
	print "All done!"
