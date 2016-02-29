"""Reads and writes SoftFiles to disk.
"""


import os.path
import time

from . import geo_downloader
from . import cleaner


BASE_DIR = 'g2e/static/softfile/'
TESTS_DATA_DIR = 'g2e/static/softfile/example/'
CLEANED_DIR = BASE_DIR + 'clean/'
EXAMPLE_FILE = 'example_input.txt'
EXT = '.txt'


def write(name, platform, normalize, genes, a_vals, b_vals, samples, selections, stats):
    """Writes the contents of a SoftFile to disk and returns a relative path.
    """
    print 'Writing clean SOFT file.'

    ab_vals = cleaner.concat(a_vals, b_vals)
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
    if isinstance(file_obj, file):
        full_path = BASE_DIR + EXAMPLE_FILE
        return full_path[4:]

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


def download(accession):
    """Downloads file from GEO.
    """
    file_path = path(accession)
    geo_downloader.download(accession, file_path)


def get(name):
    """Returns file object from disk.
    """
    return open(BASE_DIR + name + EXT).read()


def get_example_file():
    """Returns an example file with synthetic gene expression data.
    """
    with open(TESTS_DATA_DIR + EXAMPLE_FILE, 'r') as fin, open(BASE_DIR + EXAMPLE_FILE, 'w+') as fout:
        for line in fin:
            fout.write(line)
    return open(BASE_DIR + EXAMPLE_FILE)


def _build_selections(selections):
    """Handles the ordering of the columns based on control vs. sample.
    """
    # In soft_file_factory.parser, we find all the control columns and put
    # them first (leftmost) and then the condition columns and put them next
    # (rightmost).
    return ['0' for x in selections['a_indices']] + \
           ['1' for x in selections['b_indices']]
