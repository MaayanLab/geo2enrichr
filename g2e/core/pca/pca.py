"""Delegates to principal component analysis module.
"""


import pandas
import numpy as np
from sklearn import decomposition

from g2e.db import dataaccess
from g2e.core.softfile.softcleaner import avg_dups


def from_gene_signatures(extraction_ids):
    data_frames = []
    for extraction_id in extraction_ids:

        # TODO: Fetch all gene signatures with a single DB query.
        gene_sig = dataaccess.fetch_gene_signature(extraction_id)
        genes = []
        values = []
        for rg in gene_sig.gene_lists[2].ranked_genes:
            genes.append(rg.gene.name)
            values.append([rg.value])

        # In principle, there should never be duplicates in our gene lists,
        # but an earlier version of GEO2Enrichr accidentally did not average
        # duplicates. Thus, any extraction ID for which this is the case will
        # fail if this step is not performed.
        indices, data = avg_dups(np.array(genes), np.array(values))
        new_df = pandas.DataFrame(
            index=indices,
            data=[x[0] for x in data]
        )
        data_frames.append(new_df)

    df = pandas.concat(data_frames, axis=1)
    df = df.fillna(0)
    pca_coords, variance_explained = compute_pca(df.T)

    series = [{'name': 'Gene signatures', 'data': []}]
    for i, (x,y,z) in enumerate(pca_coords):
        key = extraction_ids[i]
        series[0]['data'].append({'x': x, 'y': y, 'z': z, 'name': key})

    pca_obj = {'series': series}

    # This is common with `from_soft_file`. Abstract it?
    max_vals = np.max(pca_coords, axis=0)
    min_vals = np.min(pca_coords, axis=0)
    ranges = np.vstack((max_vals*1.1, min_vals*1.1))
    pca_obj['ranges'] = ranges.tolist()

    titles = ['PC%s (%.2f' %
              (i, pct) + '%' + ' variance captured)' for i, pct in enumerate(variance_explained, start=1)]
    pca_obj['titles'] = titles

    return pca_obj


def from_soft_file(soft_file):
    df = pandas.read_csv('g2e/' + soft_file.text_file, sep='\t', skiprows=8)

    genes = df.ix[:,0]
    df = df.ix[:,1:]

    if not soft_file.normalize:
        df = np.log10(df + 1.)

    # sklearn performs its analysis against a (samples, features) matrix, while
    # the SOFT file is a (features, samples) matrix.
    pca_coords, variance_explained = compute_pca(df.T)

    series = [
        {'name': 'control', 'data': []},
        {'name': 'treatment', 'data': []}
    ]
    for i, (x,y,z) in enumerate(pca_coords):
        key = soft_file.samples[i].name
        if soft_file.samples[i].is_control:
            series[0]['data'].append({'x': x, 'y': y, 'z': z, 'name': key})
        else:
            series[1]['data'].append({'x': x, 'y': y, 'z': z, 'name': key})

    pca_obj = {'series': series}

    max_vals = np.max(pca_coords, axis=0)
    min_vals = np.min(pca_coords, axis=0)
    ranges = np.vstack((max_vals*1.1, min_vals*1.1))
    pca_obj['ranges'] = ranges.tolist()

    titles = ['PC%s (%.2f' %
              (i, pct) + '%' + ' variance captured)' for i, pct in enumerate(variance_explained, start=1)]
    pca_obj['titles'] = titles

    return pca_obj


def compute_pca(df, max_components=3):
    """Performs principal component analysis and returns the first three
    principal components.
    """
    mat = df.as_matrix()
    pca = decomposition.PCA(n_components=None)

    # fit(X) - fit the model with X
    pca.fit(mat)

    # explained_variance_ratio_ - % of variance explained by each of the
    # selected components. Take only the first 3 components.
    variance_explained = pca.explained_variance_ratio_[0:max_components]
    variance_explained *= 100

    # transform(X) - apply the dimensionality reduction on X
    pca_coords = pca.transform(mat)[:, 0:max_components]

    # return the coordinates of the transformed data, plus the % of variance
    # explainced by each component
    return pca_coords, variance_explained
