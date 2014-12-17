"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
from numbers import Number

from log import pprint


def normalize(A, B, genes):
	"""Normalizes the data, taking the log2 of and quantile normalizing the
	data if necessary.
	"""

	# Raise exceptions if the A and B are not valid data sets.
	_validate(A, B)

	if not _is_log2(A, B):
		pprint('Taking the log2 of data.')
		A, B = log2(A, B)

	if not _is_norm(A, B):
		pprint('Quantile normalizing the data.')
		A, B = qnorm(A, B)

	A, B, genes = avg_dups(A, B, genes)

	# For sanity checking code.
	#with open('gse24493.txt', 'w+') as out:
	#	for i in range(len(A)):
	#		out.write(str(genes[i]) + '\t' + str(A[i]) + '\t' + str(B[i]) + '\n')

	return (A, B, genes)


def log2(A, B):
	"""Takes the log2 of every value if required.
	"""

	return (np.log2(A), np.log2(B))


def _is_log2(A, B):
	AB = np.concatenate((A, B), axis=1)
	AB_max = np.amax(AB)
	AB_min = np.amin(AB)
	if AB_max - AB_min < 100:
		return True
	return False


def qnorm(A, B):
	"""Performs quantile normalization on two arrays of arrays.
	"""

	# Quantile normalization is a 4 step algorithm to make two or more
	# distributions identical in statistical properties. Below is a
	# visualization:
	#
	#          Original    Ranked    Averaged    Re-ordered
	#          A   B       A   B     A   B       A   B
	# gene1    2 4 8 6     2 4 3 3   3 3 3 3     3 3 6 6
	# gene2    6 4 3 3     6 4 8 6   6 6 6 6     6 6 3 3
	#
	# Read more here: http://en.wikipedia.org/wiki/Quantile_normalization

	# axis=0 means that an operation runs against columns rather than rows.

	# 1. Create matrix, i.e. concatenate the rows vertically.
	O = np.hstack((A, B))

	# 2. Sorted by rank.
	M = np.sort(O, axis=0)

	# 3. Averaged.
	# axis=1 indicates that the means are calculated across rows, not columns.
	D = np.mean(M, axis=1)
	for i, avg in enumerate(D):
		M[i].fill(float(avg))

	# 4a. Ranked by index:
	# First argsort gets the order. Second argsort gets the rank. See
	# http://stackoverflow.com/a/6266510/1830334.
	I = np.argsort(np.argsort(O, axis=0), axis=0)

	# 4b. Move values back to their original locations.
	M = M.T
	I = I.T
	O = O.T
	for i in range(len(M)):
		O[i] = M[i][I[i]]
	O = O.T

	A, B = np.hsplit(O, 2)
	return (A, B)


def _is_norm(A, B):
	"""Returns True if the data appears normalized, False otherwise.
	"""

	# See http://stackoverflow.com/a/7791101/1830334 for details.

	AB = np.concatenate((A, B), axis=1)
	medians = np.median(AB, axis=0)
	medians_mean = np.mean(medians)
	stds = np.std(AB, axis=0)
	stds_mean = np.mean(stds)
	medians_std = np.std(medians, axis=0)
	stds_std = np.std(stds, axis=0)

	# TODO: You could take the max and min values rather than iterating over
	# all of them. Andrew has checked and verified this code, though, so do
	# not optimize without tests in place.
	for i, median in np.ndenumerate(medians):
		if abs((median - medians_mean) / medians_std) > 4:
			return False
	for i, std in np.ndenumerate(stds):
		if abs((std - stds_mean) / stds_std) > 4:
			return False
	return True


def avg_dups(A, B, genes):
	"""Finds duplicate genes and averages their expression data.
	"""

	pprint('Averaging any duplicates.')

	AB = np.concatenate((A, B), axis=1)
	genes = np.array(genes)
	unq_genes = np.unique(genes)
	out_AB = np.zeros((unq_genes.shape[0], AB.shape[1]))
	for i, gene in enumerate(unq_genes):
		dups = AB[genes==gene]
		out_AB[i] = np.mean(dups, axis=0)

	A, B = np.hsplit(out_AB, 2)
	return (A, B, unq_genes)


def _validate(A, B):
	if len(A) != len(B) != len(genes):
		raise ValueError('Control and experimental expression data and gene \
			symbols must have an equal number of data points.')
	if not _all_numbers(A, B):
		raise ValueError('There should be only numbers in control expression \
			data. Non-number element(s) found.')


def _all_numbers(A, B):
	"""Check if there are non-number elements in A or B. We know they are the
	same length at this point.
	"""

	for row in range(len(A)):
		for col in range(len(A[0])):
			if not isinstance(A[row][col], Number):
				return False
			if not isinstance(B[row][col], Number):
				return False
	return True