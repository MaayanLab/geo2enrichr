# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


from collections import Counter
from math import log

import numpy
from scipy import stats

import chdir
import util


def parse_soft(filename, use_chdir, control_indices=None, experimental_indices=None, control_names=None, experimental_names=None):
	pvalues = []

	# chdir variables
	gene_order = []
	control = []
	experimental = []

	removed_probes = []

	with open(filename) as soft_file:
		# skip comments
		discard = next(soft_file)
		while discard.rstrip() != '!dataset_table_begin':
			discard = next(soft_file)
		
		# read header
		header = next(soft_file)
		header = header.rstrip('\r\n').split('\t')
		
		# GWG: I'm pretty sure this is a bug in the original code.
		# It shifts the header columns, and we mis-identify the second column as a gene.
		#header = header[2:]

		# find the columns indices
		if control_indices is None and experimental_indices is None:
			control_indices = [header.index(gsm) for gsm in control_names]
			experimental_indices = [header.index(gsm) for gsm in experimental_names]

		counter = 0
		# read rest of soft
		for line in soft_file:
			counter += 1
			if counter % 1000 == 0:
				# GWG: This could be the source of server sent events?
				print counter

			split_line = line.rstrip('\r\n').split('\t')
			if split_line[0] == '!dataset_table_end' or split_line[1] == '--Control':
				continue

			symbol = split_line[1]
			values = split_line[2:]

			if 'null' in values:
				removed_probes.append((symbol, values))
				continue

			try:
				control_values      = [float(values[i]) for i in control_indices]
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
			up_threshold   = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.soft', ''))

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
				up_threshold   = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
			else:
				return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.soft', ''))

	# try uncorrected 0.01
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.01]
		if len(corrected_pvalues) > 100:
			corrected = True
			print 'Uncorrected with 0.01 cutoff'
			if use_chdir:
				down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
				up_threshold   = len(corrected_pvalues) - down_threshold
				threshold = (up_threshold, down_threshold)
			else:
				return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.soft', ''))

	# try uncorrected 0.05
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.05]
		print 'Uncorrected with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold   = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.soft', ''))				

	if use_chdir:
		chdir_scores = chdir.chdir(control, experimental, gene_order)
		chdir_scores = [x for x in chdir_scores if x[1] < down_threshold or x[1] > up_threshold]
		return util.output_into_file(chdir_scores, use_chdir, filename.replace('.soft', ''))


def parse_series_matrix(filename, use_chdir, control_indices=None, experimental_indices=None, control_names=None, experimental_names=None):
	# make list to store pvalues in later
	pvalues = []

	# chdir variables
	gene_order = []
	control = []
	experimental = []

	removed_probes = []

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
				removed_probes.append((symbol, values))
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
			return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.txt', ''))

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
				return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.txt', ''))

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
				return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.txt', ''))

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
			return util.output_into_file(corrected_pvalues, use_chdir, filename.replace('.txt', ''))

	#call chdir if requested
	if use_chdir:
		chdir_scores = chdir.chdir(control, experimental, gene_order)
		chdir_scores = [x for x in chdir_scores if x[1] < down_threshold or x[1] > up_threshold]
		return util.output_into_file(chdir_scores, use_chdir, filename.replace('.soft', ''))