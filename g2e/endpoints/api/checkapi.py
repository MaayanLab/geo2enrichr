"""Checks if a combination of accession, dataset, and selected samples has
already been processed.
"""

from flask import Blueprint, jsonify, request

from g2e import config, db


check_api = Blueprint('check_api',
                      __name__,
                      url_prefix=config.BASE_API_URL)


@check_api.route('/check', methods=['GET'])
def check_combination():
    """Checks if a combination of accession, dataset, and selected samples has
    already been processed.
    """
    try:
        tag = request.args.get('tag')
        accession = request.args.get('accession')
        controls = request.args.get('controls').split('-')
        conditions = request.args.get('conditions').split('-')

        soft_files = db.get_soft_files_by_accession(accession)
        any_matches = False
        for sf in soft_files:
            import pdb; pdb.set_trace()
            tag_matches = _tag_matches(sf.gene_signatures, tag)
            controls_match = _samples_match(controls, sf.samples, True)
            conditions_match = _samples_match(conditions, sf.samples, False)
            if tag_matches and controls_match and conditions_match:
                any_matches = True
                break

        if any_matches:
            message = ''
        else:
            message = ''
    except AttributeError:
        message = 'Incorrect arguments'

    return jsonify({
        'message': message
    })


def _tag_matches(signature, tag):
    """Returns true if any of the gene signatures
    """
    for tag in signature.tags:
        if tag.name == tag:
            return True
    return False


def _samples_match(candidates, actual, is_control):
    """
    """
    if len(actual) == 0:
        return False
    for sample in actual:
        if sample.name not in candidates:
            return False
        else:
            if is_control and not sample.is_control:
                return False
            elif not is_control and sample.is_control:
                return False
    return True
