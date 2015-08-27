"""This module contains functions for parsing SOFT files.

__authors__ = "Gregory Gundersen, Andrew Rouillard, Axel Feldmann, Kevin Hu"
__credits__ = "Avi Ma'ayan"
__contact__ = "gregory.gundersen@mssm.edu"
"""


import csv

import g2e.core.softfile.softfilemanager as softfilemanager


def parse(name, is_geo=True, platform=None, samples=None):
    """Entry point for all file parsing. If the dataset is from GEO, this
    delegates to a function that makes some basic assumptions about GEO files.
    """
    print('Parsing SOFT file.')
    full_name = softfilemanager.path(name)
    if is_geo:
        return _parse_geo(full_name, platform, samples)
    return _parse_file(full_name)


def _parse_file(filename):
    """Parses custom SOFT file, making no assumptions about the data.
    """
    genes = []
    a_vals = []
    b_vals = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # First line should be column names.
        discard = next(csvfile)
        samples = next(csvfile)
        samples = samples.strip().split('\t')

        # Convert to a string so we can use rindex next.
        indices = ''.join(samples)
        # +1 to account for the leftmost gene symbol column.
        idx = indices.index('1')+1

        for line in reader:
            genes.append(line[0])
            a_row = line[1:idx]
            b_row = line[idx:]
            a_vals.append([float(pv) for pv in a_row])
            b_vals.append([float(pv) for pv in b_row])
    return (genes, samples, a_vals, b_vals)


def _parse_geo(filename, platform, samples):
    """Parses SOFT files, discarding bad data and converting probe IDs to gene
    sybmols.
    """

    a_cols = [x.name for x in samples if x.is_control]
    b_cols = [x.name for x in samples if not x.is_control]
    
    # COL_OFFSET changes because GDS files are "curated", meaning that they
    # have their gene symbols included. GSE files do not and are 1 column
    # thinner. That said, we do not trust the DGS mapping and do the probe-to-
    # gene mapping ourselves.
    if 'GDS' in filename:
        BOF = '!dataset_table_begin'
        EOF = '!dataset_table_end'
        COL_OFFSET = 2
        a_cols = [x.upper() for x in a_cols]
        b_cols = [x.upper() for x in b_cols]
    else:
        BOF = '!series_matrix_table_begin'
        EOF = '!series_matrix_table_end'
        COL_OFFSET = 1
        # The strings are formatted like so: '"GSM..."'. This formatting
        # strips inner quotation marks.
        a_cols = ['"{}"'.format(x.upper()) for x in a_cols]
        b_cols = ['"{}"'.format(x.upper()) for x in b_cols]

    genes = []
    A = []
    B = []
    selections = {}

    # For statistics about data quality.
    discarded_lines = 0.0
    line_count = 0.0
    unconverted_probes = 0.0
    probe_count = 0.0

    try:
        with open(filename, 'r') as soft_in:
            # Skip comments.
            discard = next(soft_in)
            while discard.rstrip() != BOF:
                discard = next(soft_in)

            # Read header and set column offset.
            header = next(soft_in).rstrip('\r\n').split('\t')
            header = header[COL_OFFSET:]
            line_length = len(header)

            # Find column indices.
            A_indices = [header.index(gsm) for gsm in a_cols]
            B_indices = [header.index(gsm) for gsm in b_cols]
            selections['A_indices'] = A_indices
            selections['B_indices'] = B_indices

            for line in soft_in:
                split_line = line.rstrip('\r\n').split('\t')
                if split_line[0] == EOF or split_line[1] == '--Control':
                    continue

                probe  = split_line[0]
                values = split_line[COL_OFFSET:]

                # Perform a conservative cleanup by ignoring any rows that
                # have null values or an atypical number of columns.
                line_count += 1
                if ('' in values or
                    'null' in values or
                    'NULL' in values or
                    len(values) != line_length or
                    # Slashes denote multiple genes.
                    '\\' in probe):

                    discarded_lines += 1
                    continue

                # GSD files already contain a column with gene symbols but we
                # do not trust that mapping.
                probe_count += 1
                gene = _probe2gene(platform, probe)
                if gene is None:
                    unconverted_probes += 1
                    continue

                A_row = [float(values[i]) for i in A_indices]
                B_row = [float(values[i]) for i in B_indices]
                A.append(A_row)
                B.append(B_row)
                genes.append(gene)

        stats = {
            'unconverted_probes_pct': unconverted_probes / probe_count * 100,
            'discarded_lines_pct': discarded_lines / line_count * 100
        }

    # Is this truly exceptional?
    except IOError:
        raise IOError('Could not read SOFT file from local server.')

    return (genes, A, B, selections, stats)


def platform_supported(platform):
    """Returns True if the platform is supported, False otherwise.
    """
    # TODO: Can this not just be: `return platform in PROBE2GENE`?
    if platform not in PROBE2GENE:
        return False
    return True


def _probe2gene(platform, probe):
    """Converts probe IDs to gene symbols. Does not check if the platform is
    supported.
    """
    # Strip any potential quotation marks.
    probe = probe.replace('"', '').replace('\'', '')
    try:
        if probe in PROBE2GENE[platform]:
            return PROBE2GENE[platform][probe]
    # This should never occur, given that we check if the platform is in the
    # dictionary. But just in case.
    except AttributeError:
        return None
    return None


def build_probe_dict(platform_probesetid_genesym_file):
    """Builds an in-memory dictionary mapping platforms to probe IDs to gene
    symbols.
    """
    # Platform data collected and script written by Andrew Rouillard.
    platform_dict = {}
    with open(platform_probesetid_genesym_file) as f:
        for line in f:
            entries = line.rstrip().split('\t')
            platform = entries[0]
            probesetid = entries[1]
            genesym = entries[2]
            if platform in platform_dict:
                platform_dict[platform][probesetid] = genesym
            else:
                platform_dict[platform] = {probesetid:genesym}
    return platform_dict


# Loads a dictionary into memory for the duration of the application.
PROBE2GENE = build_probe_dict('g2e/core/softfile/probe2gene.txt')
