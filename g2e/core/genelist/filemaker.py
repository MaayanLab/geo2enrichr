"""Builds the contents of a GeneList file as a string. Flask handles the
content type.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


def get_file_contents_as_string(genelist):
    """Writes the contents of a GeneList to disk and returns a relative path.
    """
    req_metadata = genelist.gene_signature.required_metadata
    contents = ''
    contents += __line('direction', genelist.direction)
    contents += __line('num_genes', len(genelist.ranked_genes))
    contents += __line('diffexp_method', req_metadata.diff_exp_method)
    contents += __line('cutoff', req_metadata.cutoff)
    contents += __line('correction_method', req_metadata.ttest_correction_method)
    contents += __line('threshold', req_metadata.threshold)

    opt_metadata = genelist.gene_signature.optional_metadata
    for om in opt_metadata:
        if om.name != 'user_key':
            contents += __line(om.name, om.value)

    contents += '!end_metadata\n'
    for rg in genelist.ranked_genes:
        value_string = '%0.6f' % rg.value
        gene_string = rg.gene.name + '\t' + value_string + '\n'
        contents +=  gene_string
    return contents


def __line(key, val):
    """Handles line formatting.
    """
    return ('!%s\t%s\n') % (key, str(val))