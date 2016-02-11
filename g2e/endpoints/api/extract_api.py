"""API for extracting gene signatures from GEO and custom datasets.
"""

import json

from flask import Blueprint, jsonify, request
from flask.ext.cors import cross_origin
from flask.ext.login import current_user

from g2e import config, database
from g2e import signature_factory
from g2e.exceptions import AuthException
from g2e.endpoints.request_utils import get_param_as_list


extract_api = Blueprint('extract_api',
                        __name__,
                        url_prefix=config.EXTRACT_URL)


@extract_api.route('/<extraction_id>', methods=['GET'])
@cross_origin()
def get_extraction(extraction_id):
    """Handles GET request based on extraction ID.
    """
    gene_signature = database.get_gene_signature(extraction_id)
    if gene_signature is None:
        return jsonify({
            'error': 'No gene signatures with ID %s found' % extraction_id
        })
    else:
        return jsonify(gene_signature.serialize)


@extract_api.route('/geo', methods=['POST'])
@cross_origin()
def post_from_geo():
    """Handles POST requests from GEO.
    """
    args = request.form

    admin_key = args.get('adminKey')
    is_authenticated = admin_key == config.ADMIN_KEY
    if not _user_is_authenticated_for_tag(args, is_authenticated):
        raise AuthException('One of the metadata tags used is restricted.')

    response = {}
    gene_signature = signature_factory.from_geo(args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload_soft_file', methods=['POST'])
@cross_origin()
def post_file():
    """Handles POST file upload.
    """
    args = request.form

    if not _user_is_authenticated_for_tag(args, current_user.is_authenticated):
        raise AuthException('One of the metadata tags used is restricted.')

    response = {}
    gene_signature = signature_factory.from_file(request.files['file'], args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


@extract_api.route('/upload_gene_list', methods=['POST'])
@cross_origin()
def upload_gene_list():
    """Uploads gene signature and returns extraction ID.
    """
    args = json.loads(request.data)
    gene_signature = signature_factory.from_gene_list(args)
    database.save_gene_signature(gene_signature)
    link = '%s%s/%s' % (config.SERVER_URL,
                         config.RESULTS_URL,
                         gene_signature.extraction_id)
    return jsonify({
        'extraction_id': gene_signature.extraction_id,
        'link': link
    })


@extract_api.route('/example', methods=['POST'])
@cross_origin()
def example_file():
    """Handles an example SOFT file extraction.
    """
    args = request.form

    if not _user_is_authenticated_for_tag(args, current_user.is_authenticated):
        raise AuthException('One of the metadata tags used is restricted.')

    response = {}
    file_obj = signature_factory.get_example_file()
    gene_signature = signature_factory.from_file(file_obj, args)
    database.save_gene_signature(gene_signature)
    response['extraction_id'] = gene_signature.extraction_id
    return jsonify(response)


def _user_is_authenticated_for_tag(args, is_authenticated):
    """Returns False if a tag is restricted and the user is not authenticated,
    True otherwise.
    """
    tag_names = get_param_as_list(args, 'tags')
    for tag_name in tag_names:
        tag = database.get_tag_by_name(tag_name)
        # The tag may not exist yet. If so, we can safely assume it is not
        # restricted.
        if tag and tag.is_restricted and not is_authenticated:
            return False
    return True
