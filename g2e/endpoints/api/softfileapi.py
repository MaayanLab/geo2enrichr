"""Builds a GeneList file upon request.
"""

from flask import Blueprint, Response

from g2e.db import dataaccess
from g2e.config import Config


soft_file_api = Blueprint('soft_file_api',
                          __name__,
                          url_prefix=Config.SOFT_FILE_URL)


@soft_file_api.route('/<extraction_id>')
def get_genelist(extraction_id):
    """Handles GET request based on extraction ID.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    soft_file = gene_signature.soft_file.actual_text_file

    soft_file_str = ''
    for line in soft_file:
        print line
        soft_file_str += line

    response = Response(soft_file_str, mimetype='text/plain')
    return response
