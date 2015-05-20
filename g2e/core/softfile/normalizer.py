"""Normalizes, log2 transforms and quantile normalizes, the data as necessary.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np
from numbers import Number


def normalize(genes, A, B):
    """Normalizes the data, taking the log2 of and quantile normalizing the
    data if necessary.
    """
    print 'Normalizing if necessary'

    idx = len(A[0])
    values = concat(A, B)
    genes = np.array(genes)

    # Raise exceptions if the A and B are not valid data sets.
    _validate(genes, values)

    if not _is_log(values):
        genes, values = _remove_negatives(genes, values)
        print 'Taking the log2 of data.'
        values = log2(values)

    if not _is_norm(values):
        print 'Quantile normalizing the data.'
        values = qnorm(values)

    genes, values = avg_dups(genes, values)

    A = values[:,:idx].tolist()
    B = values[:,idx:].tolist()

    return (genes, A, B)


def concat(A, B):
    """Horizontally concats two matrices.
    """
    return np.concatenate((A, B), axis=1)


def log2(values):
    """Takes the log2 of every value if required.
    """
    return np.log2(values)


def _is_log(values):
    """Returns true if the values do not have range greater than 100.
    """
    vmax = np.amax(values)
    vmin = np.amin(values)
    if vmax - vmin < 100:
        return True
    return False


# Negative values are fine per se, but we cannot allow them if we log2
# transform the data.
def _remove_negatives(genes, values):
    """Removes any rows with negative values.
    """
    # Join data so gene symbols are removed along with negative values.
    X = np.column_stack([genes, values])
    
    # Boolean index, keeping only positive values.
    X = X[(values > 0).all(axis=1)]

    # Remove gene list. This should be smaller if we removed any negatives.
    genes = X[:,0]

    # GG: I don't love changing the type from float to string to float again,
    # but (1) this isn't code for the space shuttle and (2) it doesn't seem to
    # have a deleterious effect on the data. 
    values = X[:,1:].astype(np.float)
    return (genes, values)


def qnorm(values):
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

    O = values

    # 1. Sorted by rank.
    M = np.sort(O, axis=0)

    # 2. Averaged.
    D = np.mean(M, axis=1)
    for i, avg in enumerate(D):
        M[i].fill(float(avg))

    # 3. Ranked by index:
    # First argsort gets the order. Second argsort gets the rank. See
    # http://stackoverflow.com/a/6266510/1830334.
    I = np.argsort(np.argsort(O, axis=0), axis=0)

    # 4. Move values back to their original locations.
    M = M.T
    I = I.T
    O = O.T
    for i in range(len(M)):
        O[i] = M[i][I[i]]

    return O.T


def _is_norm(values):
    """Returns True if the data appears normalized, False otherwise.
    """
    # See http://stackoverflow.com/a/7791101/1830334 for details.
    medians = np.median(values, axis=0)
    medians_mean = np.mean(medians)
    stds = np.std(values, axis=0)
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


def avg_dups(genes, values):
    """Finds duplicate genes and averages their expression data.
    """
    # See http://codereview.stackexchange.com/a/82020/59381 for details.
    folded, indices, counts = np.unique(genes, return_inverse=True, return_counts=True)
    output = np.zeros((folded.shape[0], values.shape[1]))
    np.add.at(output, indices, values)
    output /= counts[:, np.newaxis]
    return folded, output


def _validate(genes, values):
    """Verifies that A and B each has an equal number of rows. This does *not*
    check--because we don't care--that there are an equal number of items in
    each column, i.e. the user selected an equal number of control and
    experimental samples.
    """
    # Both of these exceptions should only be raised in truly exceptional
    # scenarios, such as a parsing error or a problem with the data itself.
    if len(values) != len(genes):
        raise ValueError('Expression data and gene symbols are in unequal numbers.')
    if np.isnan(values).any():
        raise ValueError('There should be only numbers in control expression \
            data. Non-number element(s) found.')
