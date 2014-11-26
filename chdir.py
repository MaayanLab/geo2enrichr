import numpy as np
import warnings
import numbers

# This code caclulates the characteristic direction with regulization.

# A and B are matricies where A[i][j] is the ith gene and jth sample in A.
# r is the regulization term ranging from [0,1]. b is the characteristic direction.
# b is sorted by its components' absolute values in descending order.
# A should be the control and B be the experiment. The direction points from A to B.

# The function is an implementation of the characteristic 
# direction algorithm presented in the paper. numpy is required to run the function. 
# Please install the numpy module before using this function. This function is 
# written using python 2.7.4 and the code was tested on a Windows 7 64 bit OS

# Authors: Qiaonan Duan, Edward Chen
# Ma'ayan Lab, Icahn School of Medicine at Mount Sinai
# Jan.8, 2014
#
# Add gene symbols to results. Apr. 4, 2014
# 
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning) 

def chdir(A, B, genes, r=1, PCAMaxDimensions=50):
#  calculate a characteristic direction for a gene expression dataset 
#  A: control numeric gene expressoion data
#  B: experiment numeric gene expression data
#  b: return value, a vector of n-components, representing the characteristic
#     direction of that gene expression dataset. n equals to the number of genes 
#     in the expression dataset.
#  r: regulaized term. A parameter that smooths the covariance matrix and reduces
#     potential noise in the dataset.
#
#  PCAMaxDimensions: Adjust this parameter to set the maximum number of dimensions 
#     to reduce to. Lower means faster run time, higher means better accuracy.

 
# Note: make sure control(A) and experiment(B) have equal number of genes

	if len(A)!= len(B):
		raise RuntimeError('control expression data must have equal number of genes as experiment expression data!')
	
#check if there are non-number elements in A or B
	if not all([isinstance(element, numbers.Number) for row in A for element in row]):
		raise RuntimeError('There should be only numbers in control expression data. Non-number element(s) found in A.')
	if not all([isinstance(element, numbers.Number) for row in B for element in row]):
		raise RuntimeError('There should be only numbers in experiment expression data. Non-number element(s) found in B.')

# place control gene expression data and experiment gene expression data into
# one matrix X.
	X = np.concatenate((A,B), axis = 1).T

# get the number of samples (colCount), namely, the total number of replicates in   
# control and experiment. Also get the number of genes (rowCount)
	(rowCount,colCount) = np.shape(X)

#  the number of output components desired from PCA. We only want to calculate
#  the chdir in a subspace that capture most variance in order to save computation 
#  workload. The number is set 20 because considering the number of genes usually 
#  present in an expression matrix 20 components would  capture most of the variance.
	maxComponentsNum = min(PCAMaxDimensions, rowCount - 1)

# use the nipals PCA algorithm to calculate scores, loadings, and explained_var. 
# explained_var are the variances captured by each component 
	scores, loadings, explained_var = nipals(X,maxComponentsNum,1e5,1e-4)

# We only want components that cpature 95% of the total variance or a little above.
	cumVariance = np.cumsum(explained_var)
	keepIdx = min(sum(cumVariance<0.95)+1, len(cumVariance))

# slice scores and loadings to only that number of components.
	scores = scores[:, :keepIdx] # R in Neil's algorithm
	loadings = loadings[:, :keepIdx] # V in Neil's algorithm
	
# the difference between experiment mean vector and control mean vector.
	meanvec = np.mean(B,axis=1) - np.mean(A,axis=1)

# All the following steps calculate shrunkMats. Refer to Neil's paper for detail.
# ShrunkenMats are the covariance matrix that is placed as denominator
# in LDA formula. Notice the shrunkMats here is in the subspace of those components
# that capture about 95% of total variance.
	Dd = np.dot(scores.T,scores)/rowCount
	sigma = np.mean(np.diag(Dd))
	Dd = Dd*np.eye(*np.shape(Dd))
	shrunkMats = np.linalg.inv( r*Dd + sigma*(1-r)*np.eye(*np.shape(Dd)))

# The LDA formula.
# np.dot(np.dot(loadings,shrunkMats),loadings.T) transforms the covariance 
# matrix from the subspace to full space.
	b = np.dot(np.dot(np.dot(loadings,shrunkMats),loadings.T),meanvec)

# normlize b to unit vector
	b /= np.linalg.norm(b)

# sort b and genes by the absolute values of b's components in descending order.
	res = sorted(zip(genes, b),  key=lambda x: abs(x[1]), reverse=True)
	
	return res

def printi(arr):
	#Pretty print an array
 	print np.array_str(np.array(arr))

def nipals(X,a,it=100,tol=1e-4):
	# Nipals algorithm for Principal Component Analysis
	# This function is written largely based on nipals function from R chemometrics package.
	
	(obsCount,varCount) = np.shape(X)
	Xh = X - np.mean(X,axis=0)
	T = np.zeros((obsCount,a))
	P = np.zeros((varCount,a))
	pcvar = np.zeros(varCount)
	varTotal = np.sum(np.var(Xh,axis=0))
	currVar = varTotal
	nr = 0

	for h in range(a):
		th = np.reshape(Xh[:,0],(obsCount,-1))
		ende = False

		while not ende:
			nr = nr + 1
			ph = np.dot(Xh.T,th)/np.dot(th.T,th)
			ph = ph/np.linalg.norm(ph)
			thnew = np.dot(Xh,ph)/np.dot(ph.T,ph)
			prec = np.dot((thnew-th).T,(thnew-th))
			th = thnew

			if prec <= np.power(tol,2):
				ende = True
			if it <= nr:
				ende = True
				#print 'Iteration stops without convergence'

		Xh = Xh - np.dot(th,ph.T)
		T[:,h] = th[:,0]
		P[:,h] = ph[:,0]
		oldVar = currVar
		currVar = np.sum(np.var(Xh,axis=0))
		pcvar[h] = ( oldVar - currVar )/varTotal
		nr = 0

	return T, P, pcvar
  