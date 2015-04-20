import numpy as np
import mlpy
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

# A and B are matricies where A[i][j] is the ith gene and jth sample in A
# There are p genes in the microarray where 1 <= i <= p
# Let number of samples in each class to be n_a and n_b
def chdir(identifiers, A, B, threshold=0.40, standarization=False):
	assert len(A) == len(B)
	# remove mean of each row
	# x_prime = []
	# for i in range(len(A)):
	# 	row = A[i] + B[i]
	# 	mean = sum(row) / float(len(row))
	# 	x_prime.append([value-mean for value in row])

	# make combined matrix
	X = []
	for i in range(len(A)):
		X.append(A[i] + B[i])
	X = np.array(X).T
	print 'before removing constant genes'
	# remove constant genes
	genesVar = np.var(X,axis=0)
	constantIdx = np.where(genesVar==0)[0]
	X = np.delete(X,constantIdx,axis=1)
	identifiers = [identifiers[i] for i in range(len(identifiers))
		if i not in constantIdx]

	print 'starting row count'
	(rowCount,colCount) = np.shape(X)
	if 20 > colCount:
		maxComponentsNum = colCount
	else:
		maxComponentsNum = 20
	print 'nipals'
	scores, loadings, explained_var = nipals(X,maxComponentsNum,1e5,1e-4)
	scores = scores.T
	loadings = loadings.T

	# want only 0.999 of captured variance
	captured_variance = 0
	for i in range(len(explained_var)):
		captured_variance += explained_var[i]
		if captured_variance > 0.999:
			break

	scores = scores[0:i+1]
	loadings = loadings[0:i+1]


	# run linear discriminant analysis classification
	ldac = mlpy.LDAC()
	ldac.learn(scores.T, np.array([1]*len(A[0]) + [2]*len(B[0])))
	w = ldac.w()

	b_full = np.dot(w,loadings)
	b_full /= np.linalg.norm(b_full)	# normalize
	
	ranked_ids = zip(identifiers, b_full)
	ranked_ids = sorted(ranked_ids, key=lambda x: x[1], reverse=True)
	print ranked_ids[0:20]

	running_sum = 0
	included_ids = []
	print threshold
	for identifier, score in ranked_ids:
		running_sum += 1
		if running_sum > threshold[0]:
			break
		else:
			included_ids.append((identifier, score))

	ranked_ids.reverse()
	print ranked_ids[0:20]
	running_sum = 0
	for identifier, score in ranked_ids:
		running_sum += 1
		if running_sum > threshold[1]:
			break
		else:
			included_ids.append((identifier, score))
				
	return included_ids

def printi(arr):
	print np.array_str(np.array(arr))

def nipals(X,a,it=100,tol=1e-4):

	X = np.array(X)
	(obsCount,varCount) = np.shape(X)
	Xh = X - np.tile(np.mean(X,axis=0),(obsCount,1))
	T = np.zeros((obsCount,a))
	P = np.zeros((varCount,a))
	pcvar = np.zeros(varCount)
	varTotal = np.sum(np.var(Xh,axis=0))
	currVar = varTotal
	nr = 0
	counter = 0
	for h in range(a):
		counter += 1
		if counter % 1000 == 0:
			print counter
		th = np.reshape(Xh[:,0],(obsCount,-1))
		ende = False

		while not ende:
			nr = nr + 1
			ph = np.dot(Xh.T,th)/np.dot(th.T,th)
			ph = ph/np.sqrt(np.dot(ph.T,ph))
			thnew = np.dot(Xh,ph)/np.dot(ph.T,ph)
			prec = np.dot((thnew-th).T,(thnew-th))
			th = thnew

			if prec <= np.power(tol,2):
				ende = True
			if it <= nr:
				ende = True
				print 'Iteration stops without convergence'

		Xh = Xh - np.dot(th,ph.T)
		T[:,h] = th[:,0]
		P[:,h] = ph[:,0]
		oldVar = currVar
		currVar = np.sum(np.var(Xh,axis=0))
		pcvar[h] = ( oldVar - currVar )/varTotal
		nr = 0

	return T, P, pcvar







