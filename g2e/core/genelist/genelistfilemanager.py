"""This module handles reading and writing GeneLists to disk.
"""


import os.path


BASE_DIR = 'static/genelist/'
EXT = '.txt'


def write(name, ranked_genes):
    """Writes the contents of a SoftFile to disk and returns a relative path.
    """
    full_path = BASE_DIR + name + EXT
    with open(full_path, 'w+') as f:
        f.write('foo')
    return full_path
