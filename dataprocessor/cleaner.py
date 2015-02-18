"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
from numbers import Number

from server.log import pprint


def normalize(A, B, genes):
	"""Normalizes the data, taking the log2 of and quantile normalizing the
	data if necessary.
	"""

	# Raise exceptions if the A and B are not valid data sets.
	_validate(A, B, genes)

	if not _is_log2(A, B):
		A, B, genes = _remove_negatives(A, B, genes)
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


# Negative values are fine per se, but we cannot allow them if we log2
# transform the data.
def _remove_negatives(A, B, genes):
	"""Removes any rows with negative values.
	"""

	# Store where we need to split the matrix.
	idx = len(A[0])
	
	# Rebuild the data so we remove gene symbols when we remove negative
	# values.
	AB = np.hstack((A, B))
	X = np.column_stack([genes, AB])
	
	# Boolean index, keeping only positive values.
	X = X[(AB > 0).all(axis=1)]

	# Remove gene list. This should be smaller if we removed any negatives.
	genes = X[:,0]
	AB = X[:,1:]

	# GG: I don't love changing the type from float to string to float again,
	# but (1) this isn't code for the space shuttle and (2) it doesn't seem to
	# have a deleterious effect on the data. If we ever want it, this function
	# will create a numpy record, that can have multiple types:
	#
	#     X = np.core.records.fromarrays([genes] + [AB[:,i] for i in range(AB.shape[1])])
	#
	# I did not opt to use it because it seemed overly complicated for now.
	A = AB[:,:idx].astype(np.float)
	B = AB[:,idx:].astype(np.float)

	return (A, B, genes)


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

	# Store where we need to split the matrix.
	idx = len(A[0])

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

	#A, B = np.hsplit(O, 2)
	A = O[:,:idx]
	B = O[:,idx:]
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

	idx = len(A[0])
	AB = np.concatenate((A, B), axis=1)
	#assert(np.array_equal(A, AB[:,:idx]))
	#assert(np.array_equal(B, AB[:,idx:]))

	genes = np.array(genes)
	unq_genes = np.unique(genes)
	out_AB = np.zeros((unq_genes.shape[0], AB.shape[1]))
	for i, gene in enumerate(unq_genes):
		dups = AB[genes==gene]
		out_AB[i] = np.mean(dups, axis=0)

	#A, B = np.hsplit(out_AB, 2)
	A = out_AB[:,:idx]
	B = out_AB[:,idx:]
	return (A, B, unq_genes)


def _validate(A, B, genes):
	"""Verifies that A and B each has an equal number of rows. This does *not*
	check--because we don't care--that there are an equal number of items in
	each column, i.e. the user selected an equal number of control and
	experimental samples.
	"""

	# Both of these exceptions should only be raised in truly exceptional
	# scenarios, such as a parsing error or a problem with the data itself.
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

	# Optimization: if we know that A and B each contain rows with an equal
	# number of elements, we can iterate through them all at once. Otherwise
	# we have to iterate over them more carefully.
	#if len(A[0]) == len(B[0]):
	#	for row in range(len(A)):
	#		for col in range(len(A[0])):
	#			if not isinstance(A[row][col], Number):
	#				return False
	#			if not isinstance(B[row][col], Number):
	#				return False

	if len(A[0]) > len(B[0]):
		lower_limit = len(B[0])
		upper_limit = len(A[0])
		upper_sample = A
	# If A[0] < B[0] or if they are equal--in which case, it shouldn't matter.
	#else if len(A[0]) < len(B[0]):
	else:
		lower_limit = len(A[0])
		upper_limit = len(B[0])
		upper_sample = B
	#else:
	#	lower_limit = upper_limit = lower_sample = None

	for row in range(len(A)):
		for col in range(lower_limit):
			if not isinstance(A[row][col], Number):
				return False
			if not isinstance(B[row][col], Number):
				return False

		# Now look at the upper limits.
		for col in range(lower_limit, upper_limit):
			if not isinstance(upper_sample[row][col], Number):
				return False

	return True
