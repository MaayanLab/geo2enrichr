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

	         Original    Ranked    Averaged    Re-ordered
	         A   B
	gene1    2 4 8 6     2 4 3 3   3 3 3 3     3 3 6 6
	gene2    6 4 3 3     6 4 8 6   6 6 6 6     6 6 3 3

	Read more here: http://en.wikipedia.org/wiki/Quantile_normalization
	"""

	# axis=0 means that an operation runs against columns rather than rows.

	# 1. Create matrix, i.e. concatenate the rows vertically.
	O = np.hstack((np.array(A), np.array(B)))

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
	return (A.tolist(), B.tolist())


if __name__ == '__main__':
	A = [[2.0, 4.0, 4.0],
		[ 5.0, 4.0, 14.0],
		[1, 2, 3]]

	B = [[4.0, 6.0, 8.0],
		[ 3.0 ,5.0, 8.0],
		[ 12.0, -3.0, 0.0]]

	A, B = qnorm(A, B)