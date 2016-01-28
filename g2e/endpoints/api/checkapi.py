"""Checks if a combination of accession, dataset, and selected samples has
already been processed.
"""

from flask import Blueprint, request

from g2e.config import Config


check_api = Blueprint('check_api',
                      __name__,
                      url_prefix=Config.BASE_API_URL)


@check_api.route('/check', methods=['GET'])
def check_combination():
    """Checks if a combination of accession, dataset, and selected samples has
    already been processed.
    """
    tag = request.args.get('tag')
    accession = request.args.get('accession')
    controls = request.args.get('controls').split('-')
    conditions = request.args.get('conditions').split('-')

    print(tag)
    print(accession)
    print(controls)
    print(conditions)

    return 'checkin'




