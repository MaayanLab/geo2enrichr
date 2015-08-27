"""Handles delegating to all target applications.

__authors__ = "Gregory Gundersen"
__contact__ = "avi.maayan@mssm.edu"
"""


import time

import g2e.core.targetapp.enrichr as enrichr
import g2e.core.targetapp.l1000cds2 as l1000cds2
import g2e.core.targetapp.paea as paea
import g2e.core.targetapp.crowdsourcing as crowdsourcing


# Granular control of how many genes are sent to each downstream application.

# This is applied to every list.
ENRICHR_CUTOFF   = 1000

# These are applied only to the combined list.
L1000CDS2_CUTOFF = 2000
PAEA_CUTOFF      = 2000


# ranked_genes, 0, required_metadata, optional_metadata, soft_file, tags
def target_all_apps(ranked_genes, direction, required_metadata, optional_metadata=None, soft_file=None, tags=None):
    """Returns a dictionary of app-to-link key-value pairs.
    """
    result = { 'enrichr': '', 'l1000cds2': '', 'paea': '' }
    description = _description(direction, required_metadata)

    try:
        if required_metadata.cutoff:
            enrichr_cutoff = min(required_metadata.cutoff, ENRICHR_CUTOFF)
        else:
            enrichr_cutoff = ENRICHR_CUTOFF
        enrichr_genes = _apply_cutoff(ranked_genes, enrichr_cutoff)
        result['enrichr'] = enrichr.get_link(enrichr_genes, description)

        if direction == 0:
            # This is a hard cutoff and is also independent of user selection.
            l1000cds2_genes = _apply_cutoff(ranked_genes, L1000CDS2_CUTOFF)
            result['l1000cds2'] = l1000cds2.get_link(l1000cds2_genes, required_metadata)
            if required_metadata.diff_exp_method == 'chdir':
                paea_genes = _apply_cutoff(ranked_genes, PAEA_CUTOFF)
                result['paea'] = paea.get_link(paea_genes, description)
            crowdsourcing.post_if_necessary(
                ranked_genes, required_metadata, optional_metadata, soft_file, tags
            )

    except:
        print 'Error with target applications'
    return result


def _description(direction, required_metadata):
    """Convert the direction and required_metadata to a human readable string.
    """
    return _direction(direction) + '_' + str(required_metadata)


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
