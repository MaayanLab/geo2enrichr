from __future__ import division
import numpy as np
from scipy import interpolate

# see: scoreatpercentile


def my_interpolate(pos, v):
  """Return interpolated value pos from v.
  Args:
    pos: 0 <= x <= 1 fractional position in v
    v: [num] vector
  Returns:
    num of interpolated v @ pos
  """
  n = len(v)-1
  low, high = int(np.floor(n*pos)), int(np.ceil(n*pos))
  if low==high:
    return v[low]
  else:
    frac = pos*n - low
    return v[low]*(1-frac) + v[high]*(frac)

  
def frac_intervals(n):
  """n intervals uniformly spaced from 0 to 1 inclusive"""
  q = np.arange(0,n)/(n-1)
  q[0],q[-1] = 0, 1
  return q

def quantile_norm(M):
  """Quantile normalize masked array M in place."""
  Q = M.argsort(0, fill_value=np.inf)
  m, n = np.size(M,0), np.size(M,1)
  # np.count_nonzero changed to np.sum for numpy1.5
  counts = np.array([m - np.sum(M.mask[:,i]) for i in range(n)])

  # compute quantile vector
  quantiles = np.zeros(m)
  for i in xrange(n):
    # select first [# values] rows of argsorted column in Q
    r = counts[i] # number of non-missing values for this column
    v = M.data[:,i][Q[:r,i]] # ranks > r point to missing values == infinity
    # create linear interpolator for existing values
    f = interpolate.interp1d(np.arange(r)/(r-1), v)
    v_full = f(frac_intervals(m))

    quantiles += v_full
  quantiles = quantiles / n
  f_quantile = interpolate.interp1d(frac_intervals(m), quantiles)

  ranks = np.empty(m, int)
  for i in xrange(n):
    r = counts[i]
    ranks[Q[:,i]] = np.arange(m)
    # Get equivalence classes; unique values == 0
    dupes = np.zeros(m, dtype=np.int)
    for j in xrange(r-1):
      if M[Q[j,i],i] == M[Q[j+1,i],i]:
        dupes[j+1] = dupes[j]+1
    # zero-out ranks higher than the number of values (to prevent out of range errors)
    ranks[ranks>=r] = 0
    # Replace column with quantile ranks
    M.data[:,i] = f_quantile(ranks/(r-1))
    # Average together equivalence classes
    j = r-1
    while j >= 0:
      if dupes[j] == 0:
        j -= 1
      else:
        idxs = Q[j-dupes[j]:j+1,i]
        M.data[idxs,i] = np.median(M.data[idxs,i])
        j -= 1 + dupes[j]
    assert j == -1
    

def quantile_normalization(anarray):

        """

        anarray with samples in the columns and probes across the rows

        import numpy as np

        """

        A=anarray

        AA = np.zeros_like(A)

        I = np.argsort(A,axis=0)

        AA[I,np.arange(A.shape[1])] = np.mean(A[I,np.arange(A.shape[1])],axis=1)[:,np.newaxis]

        return AA