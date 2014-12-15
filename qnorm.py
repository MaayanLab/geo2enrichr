"""This module contains a single function to quantile normalize two matrices.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

import numpy as np


def qnorm(A, B):
	"""Performs quantile normalization on two arrays of arrays.

	Quantile normalization is a 4 step algorithm to make two or more
	distributions identical in statistical properties. Below is a
	visualization:

	Original	Ranked		Averaged	Re-ordered
	2,20		2,8			5,5			5,13
	6,8		 	6,20		13,13		13,5

	Read more here: http://en.wikipedia.org/wiki/Quantile_normalization
	"""

	# axis=0 means that an operation runs against columns rather than rows.

	# Store height so we can un-concatenate arrays later.
	h = len(A)

	# 1. Create matrix, i.e. concatenate the rows vertically.
	O = np.vstack((np.array(A), np.array(B)))	

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
	for i, row in enumerate(M):
		for j, val in enumerate(row):
			row, col = np.where(I==i)
			O[row, col] = M[i][j]

	A, B = np.vsplit(O, h)
	return (A.tolist(), B.tolist())


if __name__ == '__main__':
	A = [[2,4,4],
		[ 5,4,14]]

	B = [[4,6,8],
		[ 3,5,8]]

	A, B = qnorm(A, B)