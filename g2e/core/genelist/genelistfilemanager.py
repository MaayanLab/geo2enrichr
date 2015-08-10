"""Handles reading and writing GeneLists to disk.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os.path


BASE_DIR = 'g2e/static/genelist/'
EXT = '.txt'


def write(name, direction, ranked_genes, metadata):
    """Writes the contents of a GeneList to disk and returns a relative path.
    """
    full_path = BASE_DIR + name + EXT
    with open(full_path, 'w+') as f:
        f.write( _line('direction', direction) )
        f.write( _line('num_genes', len(ranked_genes)) )
        f.write( _line('diffexp_method', metadata.diff_exp_method) )
        f.write( _line('cutoff', metadata.cutoff) )
        f.write( _line('correction_method', metadata.ttest_correction_method) )
        f.write( _line('threshold', metadata.threshold) )
        f.write( _line('cell', metadata.cell) )
        f.write( _line('perturbation', metadata.perturbation) )
        f.write( _line('gene', metadata.gene) )
        f.write( _line('disease', metadata.disease) )
        f.write('!end_metadata\n')
        for rg in ranked_genes:
            value_string = '%0.6f' % rg.value
            gene_string = rg.gene.name + '\t' + value_string + '\n'
            f.write(gene_string)

    # slice the root directory ("g2e") because that is the same name as the
    # server endpoint; the resultant URL would be "g2e/g2e", which would be
    # incorrect.
    return full_path[4:]


def _line(key, val):
    """Handles line formatting.
    """
    return '!' + key + ':\t' + str(val) + '\n'
