"""Builds a GeneList file upon request.
"""


from flask import Blueprint, Response
from g2e.config import Config
from g2e.dataaccess import dataaccess


soft_file = Blueprint('soft_file', __name__, url_prefix=Config.SOFT_FILE_URL)


@soft_file.route('/<extraction_id>')
def get_genelist(extraction_id):
    """Handle GET request based on extraction ID.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    soft_file = gene_signature.soft_file.actual_text_file

    soft_file_str = ''
    for line in soft_file:
        print line
        soft_file_str += line

    response = Response(soft_file_str, mimetype='text/plain')
    return response
