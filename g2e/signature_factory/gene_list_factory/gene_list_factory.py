"""Creates up, down, and combined gene lists.
"""

from flask import request
from ... import database, target_applications, differential_expression
from substrate import Gene, GeneList, RankedGene


def from_soft_file(soft_file, required_metadata, optional_metadata, tags):
    """Wrapper method for creating one of each "kind" of gene list: up, down,
    and combined.
    """
    # 1. Perform differential expression analysis with no cutoff. We do
    #    perform the thresholding for the t-test since that is part of
    #    the analysis.
    ranked_genes = differential_expression.do(
        soft_file.a_vals,
        soft_file.b_vals,
        soft_file.genes,
        required_metadata
    )

    # 2. Analyze the full gene list on target applications.
    #    "f_" prefix stands for "full".
    up_genes = [t for t in ranked_genes if t.value > 0]
    down_genes = [t for t in ranked_genes if t.value < 0]

    if 'skip_target_apps' in request.form:
        target_apps_up = target_apps_down = target_apps_combined = []
    else:
        target_apps_up = target_applications.get_links(up_genes, 1, required_metadata)
        target_apps_down = target_applications.get_links(down_genes, -1, required_metadata)
        target_apps_combined = target_applications.get_links(
            ranked_genes, 0, required_metadata, optional_metadata, soft_file, tags
        )

    # 3. Apply cutoff if the differential expression method is the
    #    Characteristic Direction. We don't apply it earlier because PAEA
    #    requires the full signature.
    if required_metadata.diff_exp_method == 'chdir':
        print('Applying cutoff to the Characteristic Direction')
        ranked_genes = _apply_cutoff(ranked_genes, required_metadata.cutoff)

    # 4. Build gene lists that we will store.

    # numpy sorts the data from left-to-right, but we render the results
    # "top-to-bottom", meaning we need to reverse the lists.
    ranked_genes = [rg for rg in reversed(ranked_genes)]
    up_genes = [t for t in ranked_genes if t.value > 0]
    down_genes = [t for t in ranked_genes if t.value < 0]

    gene_lists = [
        GeneList(up_genes, 1, target_apps_up),
        GeneList(down_genes, -1, target_apps_down),
        GeneList(ranked_genes, 0, target_apps_combined)
    ]

    return gene_lists


def from_uploaded_ranked_genes(ranked_genes):
    """Creates GeneList from a list of lists, where the first element in the
    inner list is the gene symbol and the second is the value.
    """
    gene_list = [
        RankedGene(database.get_or_create(Gene, name=g[0]), g[1])
        for g in ranked_genes
    ]
    direction = 0
    target_app_links = []
    return GeneList(gene_list, direction, target_app_links)


def _apply_cutoff(ranked_genes, cutoff):
    """Applies a cutoff to both lists, assuming left-to-right
    least-to-greatest.
    """
    if cutoff is None:
        return ranked_genes
    return ranked_genes[-cutoff:]
