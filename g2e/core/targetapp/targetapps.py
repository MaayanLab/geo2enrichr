"""Handles delegating to all target applications.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


import time

import g2e.core.targetapp.enrichr as enrichr
import g2e.core.targetapp.l1000cds2 as l1000cds2
import g2e.core.targetapp.paea as paea


# Granular control of how many genes are sent to each downstream application.

# This is applied to every list.
ENRICHR_CUTOFF   = 1000

# These are applied only to the combined list.
L1000CDS2_CUTOFF = 2000
PAEA_CUTOFF      = 2000


def target_all_apps(ranked_genes, direction, metadata):
    """Returns a dictionary of app-to-link key-value pairs.
    """
    result = { 'enrichr': '', 'l1000cds2': '', 'paea': '' }
    description = _description(direction, metadata)

    try:
        if metadata.cutoff:
            enrichr_cutoff = min(metadata.cutoff, ENRICHR_CUTOFF)
        else:
            enrichr_cutoff = ENRICHR_CUTOFF
        enrichr_genes = _apply_cutoff(ranked_genes, enrichr_cutoff)
        result['enrichr'] = enrichr.get_link(enrichr_genes, description)

        if direction == 0:
            # This is a hard cutoff and is also independent of user selection.
            l1000cds2_genes = _apply_cutoff(ranked_genes, L1000CDS2_CUTOFF)
            result['l1000cds2'] = l1000cds2.get_link(l1000cds2_genes, metadata)
            if metadata.diff_exp_method.name == 'chdir':
                paea_genes = _apply_cutoff(ranked_genes, PAEA_CUTOFF)
                result['paea'] = paea.get_link(paea_genes, description)
    except:
        print 'Error with target applications'
    return result


def _description(direction, metadata):
    """Convert the direction and metadata to a human readable string.
    """
    return _direction(direction) + '_' + str(metadata)


def _direction(direction):
    """Converts an internal representation of 'direction' to a human readable
    one.
    """
    if direction == 1:
        return 'Up'
    if direction == -1:
        return 'Down'
    return 'Combined'


def _apply_cutoff(ranked_genes, cutoff):
    """Applies a cutoff to a ranked genes list, assuming left-to-right is
    least-to-greatest.
    """
    # This is a function for testing purposes.
    return ranked_genes[-cutoff:]
