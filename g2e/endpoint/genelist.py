"""Builds a GeneList file upon request.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, Response
from g2e.config import Config
from g2e.dataaccess import dataaccess
from g2e.core.genelist import filemaker


genelist = Blueprint('genelist', __name__, url_prefix=Config.BASE_URL + '/genelist')


@genelist.route('/<direction>/<extraction_id>')
def get_genelist(direction, extraction_id):
    """Handle GET request based on extraction ID.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    genelist = __get_genelist_by_direction(gene_signature, int(direction))
    genelist_str = filemaker.get_file_contents_as_string(genelist)
    response = Response(genelist_str, mimetype='text/plain')
    return response


def __get_genelist_by_direction(gene_signature, direction):
    for genelist in gene_signature.genelists:
        if genelist.direction == direction:
            return genelist
    return None