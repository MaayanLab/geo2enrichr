"""Checks if a combination of accession, dataset, and selected samples has
already been processed.
"""

from flask import Blueprint, jsonify, request

from g2e import config, database
from g2e.exceptions import HttpRequestArgumentsException
from g2e.endpoints.request_utils import get_param_as_list


check_duplicate_api = Blueprint('check_api',
                                __name__,
                                url_prefix=config.API_URL)


@check_duplicate_api.route('/check_duplicate', methods=['GET'])
def check_combination():
    """Checks if a combination of accession, dataset, and selected samples has
    already been processed.
    """
    try:
        try:
            tag = get_param_as_list(request.args, 'tags')[0]
        except IndexError as e:
            raise HttpRequestArgumentsException('Make sure you have exactly one tag.', e)
        accession = request.args.get('dataset')

        controls = get_param_as_list(request.args, 'A_cols')
        conditions = get_param_as_list(request.args, 'B_cols')
        if len(controls) == 0:
            raise HttpRequestArgumentsException('Please select 2 or more control samples.')
        if len(conditions) == 0:
            raise HttpRequestArgumentsException('Please select 2 or more condition samples.')

        soft_files = database.get_soft_files_by_accession(accession)
        matching_ids = []
        for sf in soft_files:
            tag_matches = _tag_matches(sf.gene_signature, tag)
            controls_match = _samples_match(controls, sf.samples, True)
            conditions_match = _samples_match(conditions, sf.samples, False)
            if tag_matches or controls_match or conditions_match:
                matching_ids.append(sf.gene_signature.extraction_id)

        if len(matching_ids) > 0:
            links = []
            for id_ in matching_ids:
                link = '%s%s/%s' % (config.SERVER_URL,config.RESULTS_URL, id_)
                links.append(link)
            return jsonify({
                'preexisting': True,
                'links': links
            })
        else:
            return jsonify({
                'preexisting': False
            })
    except AttributeError as e:
        raise HttpRequestArgumentsException('Illegal arguments. Make sure you have only input one tag.', e)




def _tag_matches(signature, tag_name):
    """Returns true if any of the gene signatures
    """
    for tag in signature.tags:
        if tag.name == tag_name:
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
