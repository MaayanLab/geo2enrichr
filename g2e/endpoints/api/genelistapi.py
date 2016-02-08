"""API for building/fetching gene list file.
"""

from flask import Blueprint, Response

from g2e import config, db
from g2e.pipelines.genelistutils import filemanager


gene_list_api = Blueprint('gene_list_api',
                         __name__,
                         url_prefix=config.GENE_LIST_URL)


@gene_list_api.route('/<direction>/<extraction_id>')
def get_gene_list(direction, extraction_id):
    """Returns gene list in plain text file based on gene signature ID.
    """
    gene_signature = db.get_gene_signature(extraction_id)
    genelist = _get_gene_list_by_direction(gene_signature, int(direction))
    genelist_str = filemanager.get_file_contents_as_string(genelist)
    response = Response(genelist_str, mimetype='text/plain')
    return response


def _get_gene_list_by_direction(gene_signature, direction):
    """Return a gene list based on integer-signifying direction.
    """
    for gene_list in gene_signature.gene_lists:
        if gene_list.direction == direction:
            return gene_list
    return None
