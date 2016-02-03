"""Results page for an extracted gene signature.
"""

from flask import Blueprint, request, render_template
from flask.ext.login import current_user

from g2e import config, db
from g2e.core.targetapp.crowdsourcing import CROWDSOURCING_TAGS


results_page = Blueprint('results_page',
                         __name__,
                         url_prefix=config.RESULTS_PAGE_URL)


@results_page.route('/<results_id>')
def results(results_id):
    """Single entry point for extracting a gene list from a SOFT file.
    """
    gene_signature = db.get_gene_signature(results_id)
    if gene_signature is None:
        return render_template('pages/404.html')
    gene_signature = __process_extraction_for_view(gene_signature)

    use_crowdsourcing = False
    for tag in gene_signature.tags:
        if tag.name in CROWDSOURCING_TAGS:
            use_crowdsourcing = True

    show_viz = True if gene_signature.soft_file.samples else False

    # First check if the user is anonymous, because anonymous users, i.e. the
    # default user if not logged in, has no "name" attribute.
    if current_user.is_authenticated and current_user.name == 'admin':
        template = 'pages/results-admin.html'
    else:
        template = 'pages/results.html'

    return render_template(template,
                           gene_signature=gene_signature,
                           show_viz=show_viz,
                           use_crowdsourcing=use_crowdsourcing,
                           use_simple_header=True,
                           permanent_link=request.url)


def __get_direction_as_string(direction):
    """Maps integer to human-readable string for gene list direction.
    """
    if direction == 1:
        return 'Up'
    elif direction == -1:
        return 'Down'
    else:
        return 'Combined'


def __process_extraction_for_view(gene_signature):
    """Cleans ORM object in preparation for HTML view.
    """
    for gene_list in gene_signature.gene_lists:
        gene_list.direction_as_string = __get_direction_as_string(gene_list.direction)

    if gene_signature.soft_file.normalize is None or gene_signature.soft_file.normalize is False:
        gene_signature.soft_file.normalize = False
    else:
        gene_signature.soft_file.normalize = True
    return gene_signature
