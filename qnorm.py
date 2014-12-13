"""This module contains a single function to quantile normalize two matrices.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

import numpy as np

import pdb

import operator


def qnorm(A, B):
	"""
	"""

	# TODO: Condense this code while retaining legibility! It is important not
	# to create half a dozen large numpy array objects.

	# axis=0 means that an operation runs against columns rather than rows.

	# 1. Original:
	# Stack them, i.e. concatenate the rows "vertically".
	O = np.vstack((A, B))

	# 2. Ranked:
	# First argsort gets the order. Second argsort gets the rank. Keep this
	# copy for later. See http://stackoverflow.com/a/6266510/1830334.
	ordered = np.argsort(O, axis=0)
	R = np.argsort(ordered, axis=0)

	# 3. Sorted by rank:
	E = np.sort(O, axis=0)
	C = E.copy()

	# 4. Averaged:
	D = np.mean(C, axis=1)
	for i, avg in enumerate(D):
		C[i].fill(avg)

	F = np.zeros((5,3))
	for i, row in enumerate(C):
		for j, val in enumerate(row):
			#pdb.set_trace()
			row = R[i][j]
			F[row][j] = C[i][j]



	# http://stackoverflow.com/a/6835668/1830334
	print ''
	pdb.set_trace()
	__print( C[np.argsort(C[:,0])[1]] )

	#pdb.set_trace()
	return (A, B)


def __print(M):
	for r in M:
		s = ''
		for c in r:
			s += str(c)
		print s 

if __name__ == '__main__':
	A = [[2,4,4],
		[ 5,4,14]]

	B = [[4,6,8],
		[ 3,5,8],
		[ 3,3,9]]

	qnorm(A, B)