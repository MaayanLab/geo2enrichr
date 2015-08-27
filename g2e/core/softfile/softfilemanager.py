"""Reads and writes SoftFiles to disk.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os.path
import time

import g2e.core.softfile.normalizer as normalizer


BASE_DIR    = 'g2e/static/softfile/'
CLEANED_DIR = BASE_DIR + 'clean/'
EXT         = '.txt'


def write(name, platform, normalize, genes, a_vals, b_vals, samples, selections, stats):
    """Writes the contents of a SoftFile to disk and returns a relative path.
    """
    print 'Writing clean SOFT file.'

    ab_vals = normalizer.concat(a_vals, b_vals)
    gene_values_dict = { k:v for (k,v) in zip(genes, ab_vals) }

    # We add the time to the cleaned SOFT file name because not all SOFT files
    # of the same GEO accession ID will have the same *cleaned* content. Users
    # may select a variety of samples.
    entropy = str(time.time())[:10]
    full_path = CLEANED_DIR + name + '_' + entropy + EXT
    with open(full_path, 'w+') as f:
        f.write('!dataset\t' + name + '\n')
        f.write('!platform\t' + platform + '\n')
        f.write('!normalize\t' + str(normalize) + '\n')
        f.write('!unconverted_probes\t' + str(stats['unconverted_probes_pct']) + '%\n')
        f.write('!discarded_lines\t' + str(stats['discarded_lines_pct']) + '%\n')
        f.write('!end_metadata\n')
        f.write(' \t' + '\t'.join(_build_selections(selections)) + '\n')
        f.write(' \t' + '\t'.join([x.name for x in samples]) + '\n')
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
    full_path = BASE_DIR + name + EXT
    file_obj.save(full_path)
    return full_path[4:]


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


def _build_selections(selections):
    """Handles the ordering of the columns based on control vs. sample.
    """
    a_indices = selections['a_indices']
    b_indices = selections['b_indices']
    result_list = range(max(a_indices + b_indices)+1)
    for i in a_indices:
        result_list[i] = 'a'
    for i in b_indices:
        result_list[i] = 'b'
    return filter(lambda x: x == 'a' or x == 'b', result_list)
