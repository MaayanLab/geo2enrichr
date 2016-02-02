"""Builds the contents of a GeneList file as a string. Flask handles the
content type.
"""


def get_file_contents_as_string(gene_list):
    """Writes the contents of a GeneList to disk and returns a relative path.
    """
    req_metadata = gene_list.gene_signature.required_metadata
    dataset = gene_list.gene_signature.soft_file.dataset
    contents = ''
    contents += __line('direction', gene_list.direction)
    contents += __line('num_genes', len(gene_list.ranked_genes))
    contents += __line('diffexp_method', req_metadata.diff_exp_method)
    contents += __line('cutoff', req_metadata.cutoff)
    contents += __line('correction_method', req_metadata.ttest_correction_method)
    contents += __line('threshold', req_metadata.threshold)
    contents += __line('organism', dataset.organism)

    opt_metadata = gene_list.gene_signature.optional_metadata
    for om in opt_metadata:
        if om.name != 'user_key':
            contents += __line(om.name, om.value)

    contents += '!end_metadata\n'
    for rg in gene_list.ranked_genes:
        value_string = '%0.6f' % rg.value
        gene_string = rg.gene.name + '\t' + value_string + '\n'
        contents += gene_string
    return contents


def __line(key, val):
    """Handles line formatting.
    """
    return '!%s\t%s\n' % (key, str(val))
