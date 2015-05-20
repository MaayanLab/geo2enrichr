"""Calculates the characteristic direction with regulization. This code
differs from the published code in small ways in order to be more
modular. The notation "! CHANGED !" is used to denote any differences.

__authors__ = "Qiaonan Duan, Edward Chen, Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
import warnings
import numbers


def chdir(A, B, genes):
    """Wraps original Characteristic Direction method, handling sorting by
    highest coefficients.
    """
    print 'Calculating the characteristic direction.'
    A = np.array(A)
    B = np.array(B)
    genes = np.array(genes)
    A, B, genes = _throw_away_rows_without_variance(A, B, genes)
    genes, coefficients = _chdir(A, B, genes)
    genes, coefficients = _sort_by_coefficients(genes, coefficients)
    return genes, coefficients


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

warnings.filterwarnings("ignore", category=DeprecationWarning) 

def _chdir(A, B, genes, r=1):
#  calculate a characteristic direction for a gene expression dataset 
#  A: control numeric gene expressoion data
#  B: experiment numeric gene expression data
#  b: return value, a vector of n-components, representing the characteristic
#     direction of that gene expression dataset. n equals to the number of genes 
#     in the expression dataset.
#  r: regulaized term. A parameter that smooths the covariance matrix and reduces
#     potential noise in the dataset.

# * CHANGED *
# 1. All validation happens in a common function that validates data for all
#    differential expression methods.
# 2. Use numpy to concatenate A and B.

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
    if 20 > rowCount-1:
        maxComponentsNum = rowCount - 1
    else:
        maxComponentsNum = 20

# use the nipals PCA algorithm to calculate scores, loadings, and explained_var. 
# explained_var are the variances captured by each component 
    scores, loadings, explained_var = nipals(X,maxComponentsNum,1e5,1e-4)
    scores = scores.T
    loadings = loadings.T

# We only want components that cpature 95% of the total variance or a little above.
    captured_variance = 0
    for i in range(len(explained_var)):
        captured_variance += explained_var[i]
        if captured_variance > 0.95:
            break

# slice scores and loadings to only that number of components.
    scores = scores[0:i+1] # R in Neil's algorithm
    loadings = loadings[0:i+1] # V in Neil's algorithm

    scores = scores.T
    loadings = loadings.T

# the difference between experiment mean vector and control mean vector.
    meanvec = np.mean(B,axis=1) - np.mean(A,axis=1)

# All the following steps calculate shrunkMats. Refer to Neil's paper for detail.
# ShrunkenMats are the covariance matrix that is placed as denominator 
# in LDA formula. Notice the shrunkMats here is in the subspace of those components
# that capture about 95% of total variance.
    Dd = np.dot(scores.T,scores)/rowCount
    Dd = np.diag(np.diag(Dd))
    sigma = np.mean(np.diag(Dd))
    shrunkMats = np.linalg.inv( np.dot(r,Dd)+ sigma*(1-r)*np.eye(np.shape(Dd)[0]))

# The LDA formula.
# np.dot(np.dot(loadings,shrunkMats),loadings.T) transforms the covariance 
# matrix from the subspace to full space.
    b = np.dot(loadings,np.dot(shrunkMats,np.dot(loadings.T,meanvec)))

# normlize b to unit vector
    b /= np.linalg.norm(b)

# ! CHANGED !
# Do not sort the genes before returning them. This is because Neil's unit
# test data is not sorted.
# 
# ! CHANGED!
# Return values as Python list for consistent user interface.
    print 'Done chdir'
    return (genes, b.tolist())


def nipals(X,a,it=100,tol=1e-4):
    # Nipals algorithm for Principal Component Analysis
    # This function is written largely based on nipals function from R chemometrics package.
    
    X = np.array(X)
    (obsCount,varCount) = np.shape(X)
    Xh = X - np.tile(np.mean(X,axis=0),(obsCount,1))
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


def _sort_by_coefficients(genes, values):
    """Sorts two lists, one of genes and another of values, by the absolute
    value of the values.
    """
    genes = np.array(genes)
    values = np.array(values)
    ind = np.argsort( np.absolute(values) )
    genes = genes[ind]
    genes = [str(x) for x in genes]
    values = values[ind]
    return genes, values.tolist()


def _throw_away_rows_without_variance(A, B, genes):
	"""Discards rows without variance. 
	"""
    X = np.concatenate((A,B), axis=1)
    keep_rows = np.std(X, axis=1).nonzero()[0]
    return A[keep_rows,], B[keep_rows,], genes[keep_rows]
