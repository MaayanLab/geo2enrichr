"""Performs hierarchical clustering.
"""

import json

import pandas
import requests

from substrate import TargetApp
from substrate import TargetAppLink
from g2e import database


def from_soft_file(gene_signature):
    """Performs hierarchical clustering on SOFT file.
    """
    target_app_link = __get_clustergrammer_link(gene_signature)

    # Only create the link from Clustergrammer once.
    # TODO: Move into targetapp module. API should not know about this.
    if not target_app_link:
        link = __from_soft_file(gene_signature)
        link = '{0}?preview=true'.format(link)
        target_app = database.get_or_create(TargetApp, name='clustergrammer')
        target_app_link = TargetAppLink(target_app, link)
        gene_signature.gene_lists[2].target_app_links.append(
            target_app_link
        )
        database.save_gene_signature(gene_signature)

    return target_app_link.link


def __from_soft_file(gene_signature):
    data = _get_raw_data(gene_signature.soft_file)
    sf = pandas.DataFrame(data)

    ranked_genes = []
    for rg in gene_signature.gene_lists[2].ranked_genes:
        ranked_genes.append(rg.gene.name)

    # Filter SOFT file based on genes extracted from differential expression
    # analysis.
    sf = sf.loc[sf[0].isin(ranked_genes)]

    columns = []
    for col_idx in sf.columns:
        if col_idx == 0:
            continue
        column = sf.ix[:, col_idx].tolist()
        column = [float(x) for x in column]
        genes = zip(sf.ix[:, 0], column)

        # Clustergrammer expects a list of lists, rather than tuples.
        genes = [[x, y] for x, y in genes]
        gsm = gene_signature.soft_file.samples[col_idx - 1]
        columns.append({
            'col_title': gsm.name,
            'is_control': gsm.is_control,
            'link': 'todo',
            'vector': genes
        })

    link = '%s' % gene_signature.extraction_id
    payload = {
        'link': link,
        'columns': columns
    }
    headers = {'content-type': 'application/json'}
    url = 'https://amp.pharm.mssm.edu/clustergrammer/vector_upload/'
    resp = requests.post(url, data=json.dumps(payload), headers=headers)

    if resp.ok:
        print(json.loads(resp.text)['link'])
        return json.loads(resp.text)['link']
    return None


def __get_clustergrammer_link(gene_signature):
    for target_app_link in gene_signature.gene_lists[2].target_app_links:
        if target_app_link.target_app.name == 'clustergrammer':
            return target_app_link
    return None


def _get_raw_data(soft_file):
    """Returns the raw data a two-dimensional array.
    """
    results = []
    f = open('g2e/' + soft_file.text_file)
    for i, line in enumerate(f):
        if i < 8:
            continue
        line = line.strip()
        results.append(line.split('\t'))
    return results
