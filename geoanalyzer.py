# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import numpy
from scipy import stats

import chdir
from files import GEOFile
import filemanager
import geoparser


def analyze_geo_file(filename, user_options, control, experimental):
	is_GDS = 'GDS' in filename 
	if is_GDS:
		control      = [x.upper() for x in control]
		experimental = [x.upper() for x in experimental]
	else:
		control      = ['"{}"'.format(x.upper()) for x in control]
		experimental = ['"{}"'.format(x.upper()) for x in experimental]

	# TODO: Remove the GEO file after parsing it!
	try:
		if is_GDS:
			response = __analyze_soft(filename, user_options, control, experimental)
		else:
			response = __analyze_series_matrix(filename, user_options, control, experimental)
	except IOError:
		response = {
			'error': 'IOError',
			'message': 'Error reading GEO file from server'
		}

	return response


def __analyze_soft(filename, user_options, control_names, experimental_names):
	use_chdir = user_options['method'] == 'chdir'

	full_path = GEOFile.get_full_path(filename)
	HEADER_INDEX = 0
	pvalues, gene_order, control, experimental = geoparser.parse_soft_file(full_path, control_names, experimental_names, '!dataset_table_begin', '!dataset_table_end', HEADER_INDEX)

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
			return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

	# try uncorrected 0.05
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.05]
		print 'Uncorrected with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold   = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)				

	if use_chdir:
		chdir_scores = chdir.chdir(control, experimental, gene_order)
		chdir_scores = [x for x in chdir_scores if x[1] < down_threshold or x[1] > up_threshold]
		return filemanager.build_output_file(chdir_scores, use_chdir, filename)


def __analyze_series_matrix(filename, user_options, control_names, experimental_names):
	use_chdir = user_options['method'] == 'chdir'

	full_path = GEOFile.get_full_path(filename)
	HEADER_INDEX = 1
	pvalues, gene_order, control, experimental = geoparser.parse_soft_file(full_path, control_names, experimental_names, '!series_matrix_table_begin', '!series_matrix_table_end', HEADER_INDEX)

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
			return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
			return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

	#call chdir if requested
	if use_chdir:
		chdir_scores = chdir.chdir(control, experimental, gene_order)
		chdir_scores = [x for x in chdir_scores if x[1] < down_threshold or x[1] > up_threshold]
		return filemanager.build_output_file(chdir_scores, use_chdir, filename)