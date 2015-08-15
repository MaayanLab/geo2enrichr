"""Builds the contents of a GeneList file as a string. Flask handles the
content type.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


def get_file_contents_as_string(genelist):
    """Writes the contents of a GeneList to disk and returns a relative path.
    """
    metadata = genelist.gene_signature.exp_metadata
    contents = ''
    contents += __line('direction', genelist.direction)
    contents += __line('num_genes', len(genelist.ranked_genes))
    contents += __line('diffexp_method', metadata.diff_exp_method.name)
    contents += __line('cutoff', metadata.cutoff)
    contents += __line('correction_method', metadata.ttest_correction_method.name)
    contents += __line('threshold', metadata.threshold)
    contents += __line('cell', metadata.cell)
    contents += __line('perturbation', metadata.perturbation)
    contents += __line('gene', metadata.gene)
    contents += __line('disease', metadata.disease)
    contents += '!end_metadata\n'
    for rg in genelist.ranked_genes:
        value_string = '%0.6f' % rg.value
        gene_string = rg.gene.name + '\t' + value_string + '\n'
        contents +=  gene_string
    return contents


def __line(key, val):
    """Handles line formatting.
    """
    return ('!%s:\t%s\n') % (key, str(val))