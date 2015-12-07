"""Delegates to target applications.
"""


from substrate import TargetAppLink
from substrate import TargetApp

from g2e.core.targetapp import enrichr
from g2e.core.targetapp import l1000cds2
from g2e.core.targetapp import paea
from g2e.core.targetapp import crowdsourcing
from g2e.db.util import get_or_create


# Granular control of how many genes are sent to each downstream application.
# This is applied to every list.
ENRICHR_CUTOFF = 1000
# These are applied only to the combined list.
L1000CDS2_CUTOFF = 2000
PAEA_CUTOFF = 2000


# Do you see how if-else this code is? Highly conditional code often indicates
# that it can be refactored by proper data structures. Refactor this when you
# have a chance.
def target_all_apps(ranked_genes, direction, required_metadata, optional_metadata=None, soft_file=None, tags=None):
    """Returns a dictionary of app-to-link key-value pairs.
    """
    links = []
    description = _description(direction, required_metadata)

    try:
        enrichr_link = _get_enrichr_link(ranked_genes, required_metadata, description)
        if enrichr_link.link:
            links.append(enrichr_link)

        if direction == 0 and required_metadata.diff_exp_method == 'chdir':

            l1000cds2_link = _get_l1000cds2_link(ranked_genes, required_metadata)
            if l1000cds2_link.link:
                links.append(l1000cds2_link)

            paea_link = _get_paea_link(ranked_genes, description)
            if paea_link.link:
                links.append(paea_link)

        if direction == 0 and len(tags) > 0:
            crowdsourcing_link = _get_crowdsourcing_link(ranked_genes, optional_metadata, soft_file, tags)
            if crowdsourcing_link.link:
                links.append(crowdsourcing_link)
    except:
        print 'Error with target applications'

    return links


def _get_enrichr_link(ranked_genes, required_metadata, description):
    """Wrapper for enrichr module's get_link function.
    """
    enrichr_cutoff = _get_cutoff(required_metadata)
    enrichr_genes = _apply_cutoff(ranked_genes, enrichr_cutoff)
    link = enrichr.get_link(enrichr_genes, description)
    target_app = get_or_create(TargetApp, name='enrichr')
    return TargetAppLink(target_app, link)


def _get_l1000cds2_link(ranked_genes, required_metadata):
    """Wrapper for l1000cds2 module's get_link function.
    """
    # This is a hard cutoff and is also independent of user selection.
    l1000cds2_genes = _apply_cutoff(ranked_genes, L1000CDS2_CUTOFF)
    link = l1000cds2.get_link(l1000cds2_genes, required_metadata)
    target_app = get_or_create(TargetApp, name='l1000cds2')
    return TargetAppLink(target_app, link)


def _get_paea_link(ranked_genes, description):
    """Wrapper for paea module's get_link function.
    """
    paea_genes = _apply_cutoff(ranked_genes, PAEA_CUTOFF)
    link = paea.get_link(paea_genes, description)
    target_app = get_or_create(TargetApp, name='paea')
    return TargetAppLink(target_app, link)


def _get_crowdsourcing_link(ranked_genes, optional_metadata, soft_file, tags):
    """Wrapper for crowdsourcing module's get_link function.
    """
    link = crowdsourcing.get_link(ranked_genes, optional_metadata, soft_file, tags)
    target_app = get_or_create(TargetApp, name='crowdsourcing')
    return TargetAppLink(target_app, link)


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


def _get_cutoff(required_metadata):
    if required_metadata.cutoff:
        return min(required_metadata.cutoff, ENRICHR_CUTOFF)
    return ENRICHR_CUTOFF
