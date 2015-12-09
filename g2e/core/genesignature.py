"""Transforms user input to GeneSignature instance.
"""

from substrate import GeneSignature
from g2e.core import genelistutils, optionalmetadata, softutils, requiredmetadata, tag


def create(soft_file, args):
    """Creates a new extraction, as opposed to an extraction from the
    database.
    """
    required_metadata = requiredmetadata.from_args(args)
    optional_metadata = optionalmetadata.from_args(args)
    tags = tag.from_args(args)

    gene_lists = genelistutils.from_soft_file(
        soft_file,
        required_metadata,
        optional_metadata, tags
    )
    return GeneSignature(
        soft_file,
        gene_lists,
        required_metadata,
        optional_metadata, tags
    )


def from_geo(args):
    """Creates an extraction from GEO data.
    """
    soft_file = softutils.maker.from_geo(args)
    return create(soft_file, args)


def from_file(file_obj, args):
    """Creates an extraction from a custom, uploaded SOFT file.
    """
    soft_file = softutils.maker.from_file(file_obj, args)
    return create(soft_file, args)
