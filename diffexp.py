"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy
from scipy import stats

import chdir
import filemanager

import pdb


def analyze(control_values, experimental_values, genes, config):

	# 1. Quantile normalize the data.
	# 2. Identify differentially expressed genes through a variety of methods.
	# 3. Optionally cutoff or correct the data, eliminating the least significant genes.

	use_chdir = config['method'] == 'chdir'
	#if not use_chdir:
	if False:
		return __ttest(control_values, experimental_values, genes)
	else:
		return __chdir(control_values, experimental_values, genes)


def __chdir(control, experimental, genes):
	try:
		scores = chdir.chdir(control, experimental, genes)
	except MemoryError:
		raise MemoryError('Ran out of memory performing characteristic direction.')
	#scores = [x for x in scores if x[1] < down_threshold or x[1] > up_threshold]
	return scores


def __ttest(control, experimental, genes, use_chdir):
	# sort pvalues# perform ttest
	
	#ttest_results = stats.ttest_ind(experimental_values, control_values)
	#signed_pvalue = ttest_results[1] if ttest_results[0] > 0 else ttest_results[1]*-1
	#pvalues.append((symbol, signed_pvalue))
	







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
			return corrected_pvalues
			#return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return corrected_pvalues
				#return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

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
				return corrected_pvalues
				#return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)

	# try uncorrected 0.05
	if not corrected:
		corrected_pvalues = [x for x in pvalues if abs(x[1]) < 0.05]
		print 'Uncorrected with 0.05 cutoff'
		if use_chdir:
			down_threshold = len([x for x in corrected_pvalues if x[1] < 0])
			up_threshold   = len(corrected_pvalues) - down_threshold
			threshold = (up_threshold, down_threshold)
		else:
			return corrected_pvalues
			#return filemanager.build_output_file(corrected_pvalues, use_chdir, filename)