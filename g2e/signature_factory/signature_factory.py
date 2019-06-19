"""Transforms user input to GeneSignature instance.
"""

from substrate import GeneSignature, Resource
from ..signature_factory import gene_list_factory, soft_file_factory
from .. import database
from ..exceptions import HttpRequestArgumentsException
from . import optional_metadata_factory, required_metadata_factory, tag_factory


def from_geo(args):
    """Creates gene signature from GEO data.
    """
    soft_file = soft_file_factory.soft_file_factory.from_geo(args)
    return _create_gene_signature(soft_file, args)


def from_file(file_obj, args):
    """Creates an extraction from a custom, uploaded SOFT file.
    """
    soft_file = soft_file_factory.soft_file_factory.from_file(file_obj, args)
    return _create_gene_signature(soft_file, args)


def from_gene_list(args):
    """Creates gene signature from a pre-existing gene list, not expression
    data.
    """
    ranked_genes = args.get('ranked_genes', [])
    gene_list = gene_list_factory.from_uploaded_ranked_genes(ranked_genes)

    try:
        required_metadata = required_metadata_factory.from_http_request(args)
    except Exception as e:
        raise HttpRequestArgumentsException('Error in required metadata '
                                            'fields', e)

    try:
        optional_metadata = optional_metadata_factory.from_http_request(args)
    except Exception as e:
        raise HttpRequestArgumentsException('Error in optional metadata '
                                            'fields', e)

    try:
        tags = tag_factory.from_http_request(args)
    except Exception as e:
        raise HttpRequestArgumentsException('Error in metadata tags', e)

    resource = database.get_or_create(Resource,
                                      code='upload',
                                      name='User uploaded gene list')

    return GeneSignature(None,
                         [gene_list],
                         required_metadata,
                         optional_metadata,
                         tags,
                         resource)


def _create_gene_signature(soft_file, args):
    """Creates a new extraction, as opposed to an extraction from the
    database.
    """
    required_metadata = required_metadata_factory.from_http_request(args)
    optional_metadata = optional_metadata_factory.from_http_request(args)
    tags = tag_factory.from_http_request(args)

    gene_lists = gene_list_factory.from_soft_file(
        soft_file,
        required_metadata,
        optional_metadata, tags
    )
    return GeneSignature(
        soft_file,
        gene_lists,
        required_metadata,
        optional_metadata,
        tags,
        database.get_or_create(Resource, code='geo')
    )
