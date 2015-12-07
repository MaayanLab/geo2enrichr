"""Transforms user input to GeneSignature instance.
"""


from substrate import GeneSignature, OptionalMetadata, RequiredMetadata,\
    SoftFile, Tag

from g2e.core.genelist.genelistsmaker import genelists_maker
from g2e.transformations import softfile, optionalmetadata, requiredmetadata,\
    tag


def create(soft_file, args):
    """Creates a new extraction, as opposed to an extraction from the
    database.
    """
    required_metadata = requiredmetadata.from_args(args)
    optional_metadata = optionalmetadata.from_args(args)
    tags = tag.from_args(args)

    gene_lists = genelists_maker(soft_file, required_metadata,
                                 optional_metadata, tags)
    return GeneSignature(soft_file, gene_lists, required_metadata,
                         optional_metadata, tags)


def from_geo(args):
    """Creates an extraction from GEO data.
    """
    soft_file = softfile.from_geo(args)
    return create(soft_file, args)


def from_file(file_obj, args):
    """Creates an extraction from a custom, uploaded SOFT file.
    """
    soft_file = softfile.from_file(file_obj, args)
    return create(soft_file, args)
