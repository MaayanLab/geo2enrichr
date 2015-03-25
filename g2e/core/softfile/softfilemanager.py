"""This module handles reading and writing SoftFiles to disk.
"""


import os.path

import g2e.core.softfile.normalizer as normalizer


BASE_DIR    = 'g2e/static/softfile/'
CLEANED_DIR = BASE_DIR + 'clean/'
EXT         = '.txt'


def write(name, genes, A, B):
    """Writes the contents of a SoftFile to disk and returns a relative path.
    """
    AB = normalizer.concat(A, B)
    gene_values_dict = { k:v for (k,v) in zip(genes, AB) }

    # PURPLE_WIRE: We need to not overwrite existing SoftFiles!
    print 'Writing clean SOFT file.'
    full_path = CLEANED_DIR + name + EXT
    with open(full_path, 'w+') as f:
        f.write('!datset\t' + name + '\n')
        #f.write('!platform\t' + self.platform + '\n')
        #f.write('!unconverted_probes_pct\t' + str(self.stats['unconverted_probes_pct']) + '\n')
        #f.write('!discarded_lines_pct\t' + str(self.stats['discarded_lines_pct']) + '\n')
        f.write('!end_metadata\n')
        #f.write('GENE SYMBOL\t' + '\t'.join(self.gsms) + '\n')
        for gene, val in gene_values_dict.items():
            val_str = '\t'.join(map(str, val))
            f.write(gene + '\t' + val_str + '\n')

    # slice the root directory ("g2e") because that is the same name as the
    # server endpoint; the resultant URL would be "g2e/g2e", which would be
    # incorrect.
    return full_path[4:]


def save(name, file_obj):
    """Saves a SOFT file in the correct directory.
    """
    full_path =  BASE_DIR + name + EXT
    file_obj.save(full_path)
    return full_path


def file_exists(name):
    """Returns True if the SoftFile exists on the server, False otherwise.
    """
    if os.path.isfile(BASE_DIR + name):
        return True
    return False


def path(name):
    """Returns a relative path to the SoftFile on the server.
    """
    return BASE_DIR + name + EXT
