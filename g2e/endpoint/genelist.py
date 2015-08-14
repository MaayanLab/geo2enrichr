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
    extraction = dataaccess.fetch_extraction(extraction_id)
    genelist = __get_genelist_by_direction(extraction, int(direction))
    genelist_str = filemaker.get_file_contents_as_string(genelist)
    response = Response(genelist_str, mimetype='text/plain')
    return response


def __get_genelist_by_direction(extraction, direction):
    for genelist in extraction.genelists:
        if genelist.direction == direction:
            return genelist
    return None