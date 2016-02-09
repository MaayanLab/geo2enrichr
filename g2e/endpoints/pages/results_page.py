"""Results page for an extracted gene signature.
"""

import json

from flask import Blueprint, request, render_template, redirect, url_for
from flask.ext.login import current_user, login_required
from g2e import config, database
from g2e.endpoints import request_utils
from g2e.target_applications.crowdsourcing import CROWDSOURCING_TAGS
from substrate import OptionalMetadata, Tag


results_page = Blueprint('results_page',
                         __name__,
                         url_prefix=config.RESULTS_URL)


@results_page.route('/<extraction_id>', methods=['GET'])
def view_result(extraction_id):
    """Renders extracted gene signature and associated metadata.
    """
    import pdb; pdb.set_trace()
    gene_signature = database.get_gene_signature(extraction_id)
    if gene_signature is None:
        return render_template('pages/404.html')
    gene_signature = _process_extraction_for_view(gene_signature)

    use_crowdsourcing = False
    for tag in gene_signature.tags:
        if tag.name in CROWDSOURCING_TAGS:
            use_crowdsourcing = True

    if gene_signature.soft_file and gene_signature.soft_file.samples:
        show_viz = True
    else:
        show_viz = False

    if current_user.is_authenticated and current_user.name == 'admin':
        show_admin_controls = True
        tag_names = [t.name for t in gene_signature.tags]
    else:
        show_admin_controls = False
        tag_names = None

    if gene_signature.is_from_geo:
        return render_template('pages/results.html',
                               show_admin_controls=show_admin_controls,
                               tag_names=json.dumps(tag_names),
                               gene_signature=gene_signature,
                               show_viz=show_viz,
                               use_crowdsourcing=use_crowdsourcing)
    else:
        return render_template('pages/results-not-from-geo.html',
                               show_admin_controls=show_admin_controls,
                               tag_names=json.dumps(tag_names),
                               gene_signature=gene_signature)


@results_page.route('/<extraction_id>/delete', methods=['POST'])
@login_required
def delete_result(extraction_id):
    """Deletes gene signature by extraction ID.
    """
    database.delete_gene_signature(extraction_id)
    return redirect(url_for('menu_pages.index_page'))


@results_page.route('/<extraction_id>/edit', methods=['POST'])
@login_required
def edit_result(extraction_id):
    """Edits gene signature, removing fields that are empty and adding new ones.
    """
    extraction_id = request.form.get('extraction_id')
    gene_signature = database.get_gene_signature(extraction_id)

    for opt_meta in gene_signature.optional_metadata:
        value = request.form.get(opt_meta.name)
        if not value:
            database.delete_object(opt_meta)
            continue
        opt_meta.value = value
        database.update_object(opt_meta)

    # Generate a new optional metadata field is requested.
    new_meta_name = request.form.get('new_metadata_name')
    new_meta_value = request.form.get('new_metadata_value')
    if new_meta_name and new_meta_value:
        new_opt_meta = OptionalMetadata(new_meta_name, new_meta_value)
        gene_signature.optional_metadata.append(new_opt_meta)
        database.update_object(gene_signature)

    # Update existing tags.
    tag_names = request_utils.get_param_as_list(request.form, 'tags')
    for tag in gene_signature.tags:
        if tag.name not in tag_names:
            database.delete_object(tag)
        else:
            tag_names.remove(tag.name)

    # Cretae any new tags. Note that any leftover tags are new ones.
    if len(tag_names) > 0:
        for tag_name in tag_names:
            tag = Tag(tag_name)
            gene_signature.tags.append(tag)
        database.update_object(gene_signature)

    return redirect(url_for('results_page.view_result',
                            extraction_id=extraction_id))


def _process_extraction_for_view(gene_signature):
    """Cleans ORM object in preparation for HTML view.
    """
    for gene_list in gene_signature.gene_lists:
        gene_list.direction_as_string = _get_direction_as_string(gene_list.direction)

    if gene_signature.soft_file:
        if gene_signature.soft_file.normalize is None or gene_signature.soft_file.normalize is False:
            gene_signature.soft_file.normalize = False
        else:
            gene_signature.soft_file.normalize = True
    return gene_signature


def _get_direction_as_string(direction):
    """Maps integer to human-readable string for gene list direction.
    """
    if direction == 1:
        return 'Up'
    elif direction == -1:
        return 'Down'
    else:
        return 'Combined'
