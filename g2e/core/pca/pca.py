"""Performs principal component analysis on an input SOFT file.

__authors__ = "Gregory Gundersen, Zichen Wang"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import json
import pandas
import numpy as np
from sklearn import decomposition


def do_pca(soft_file):
    df = pandas.read_csv('g2e/' + soft_file.text_file, sep='\t', skiprows=8)
    pca_coords, variance_explained = compute_pca(df)

    series = []
    for row in df.iterrows():
        obj = {}
        data = []
        x,y,z = pca_coords[row[0]]
        data.append({'x':x, 'y':y, 'z':z})
        obj['data'] = data
        series.append(obj)

    import pdb; pdb.set_trace()

    pca_obj = {'series': series}

    max_vals = np.max(pca_coords, axis=0)
    min_vals = np.min(pca_coords, axis=0)

    ranges = np.vstack((max_vals*1.1, min_vals*1.1))
    pca_obj['ranges'] = ranges.tolist()

    titles = ['PC%s (%.2f'%(i, pct) + '%' + ' variance captured)' for i, pct in enumerate(variance_explained, start=1)]
    pca_obj['titles'] = titles

    return json.dumps(pca_obj)


def compute_pca(df):
    mat = df.as_matrix()
    mat_wo_genes = mat[:,1:]
    pca = decomposition.PCA(n_components=None)
    pca.fit(mat_wo_genes)
    variance_explained = pca.explained_variance_ratio_[0:3]
    variance_explained *= 100
    pca_coords = pca.transform(mat_wo_genes)[:, 0:3]
    return pca_coords, variance_explained
