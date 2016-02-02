"""Builds a GeneList file upon request.
"""

from flask import Blueprint, Response

from g2e import config, db


soft_file_api = Blueprint('soft_file_api',
                          __name__,
                          url_prefix=config.SOFT_FILE_URL)


@soft_file_api.route('/<extraction_id>')
def get_soft_file(extraction_id):
    """Returns SOFT file in plain text file based on gene signature ID.
    """
    gene_signature = db.get_gene_signature(extraction_id)
    soft_file = gene_signature.soft_file.actual_text_file
    soft_file_str = ''
    for line in soft_file:
        print line
        soft_file_str += line
    response = Response(soft_file_str, mimetype='text/plain')
    return response
