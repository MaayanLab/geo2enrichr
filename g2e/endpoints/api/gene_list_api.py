"""API for building/fetching gene list file.
"""

from flask import Blueprint, Response

from g2e import config, database
from g2e.signature_factory.gene_list_factory import file_manager


gene_list_api = Blueprint('gene_list_api',
                         __name__,
                         url_prefix=config.GENE_LIST_URL)


@gene_list_api.route('/<direction>/<extraction_id>')
def get_gene_list(direction, extraction_id):
    """Returns gene list in plain text file based on gene signature ID.
    """
    gene_signature = database.get_gene_signature(extraction_id)
    gene_list = _get_gene_list_by_direction(gene_signature, int(direction))
    gene_list_str = file_manager.get_file_contents_as_string(gene_list)
    response = Response(gene_list_str, mimetype='text/plain')
    return response


def _get_gene_list_by_direction(gene_signature, direction):
    """Return a gene list based on integer-signifying direction.
    """
    for gene_list in gene_signature.gene_lists:
        if gene_list.direction == direction:
            return gene_list
    return None
