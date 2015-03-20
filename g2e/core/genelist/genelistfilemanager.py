"""This module handles reading and writing GeneLists to disk.
"""


import os.path


BASE_DIR = 'g2e/static/genelist/'
EXT = '.txt'


def write(name, ranked_genes, metadata):
    """Writes the contents of a GeneList to disk and returns a relative path.
    """
    full_path = BASE_DIR + name + EXT
    with open(full_path, 'w+') as f:
        f.write( _line('method', metadata.method) )
        f.write( _line('cutoff', metadata.cutoff) )
        f.write( _line('cell', metadata.cell) )
        f.write( _line('perturbation', metadata.perturbation) )
        f.write( _line('gene', metadata.gene) )
        f.write( _line('disease', metadata.disease) )
        f.write('!end_metadata\n')
        for gene,rank in ranked_genes:
            f.write('\t'.join((gene, '%0.6f' % rank)) + '\n')

    # slice the root directory ("g2e") because that is the same name as the
    # server endpoint; the resultant URL would be "g2e/g2e", which would be
    # incorrect.
    return full_path[4:]


def _line(key, val):
    return '!' + key + ':\t' + str(val) + '\n'
