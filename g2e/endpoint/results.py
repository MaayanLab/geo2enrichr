"""Single results page for an extracted gene signature.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, request, render_template
from g2e.config import Config
from g2e.dataaccess import dataaccess


results = Blueprint('results', __name__, url_prefix=Config.BASE_URL + '/results')


@results.route('/<results_id>')
def results_page(results_id):
    """Single entry point for extracting a gene list from a SOFT file.
    """
    gene_signature = dataaccess.fetch_gene_signature(results_id)
    if gene_signature is None:
        return render_template('404.html')

    gene_signature = __process_extraction_for_view(gene_signature)

    return render_template('results.html',
        tags_url=Config.BASE_TAGS_URL,
        use_simple_header=True,
        permanent_link=request.url,
        gene_signature=gene_signature
    )


def __get_direction_as_string(direction):
    if direction == 1:
        return 'Up'
    elif direction == -1:
        return 'Down'
    else:
        return 'Combined'


def __process_extraction_for_view(gene_signature):
    for gene_list in gene_signature.genelists:
        gene_list.direction_as_string = __get_direction_as_string(gene_list.direction)

    if gene_signature.softfile.normalize is None or gene_signature.softfile.normalize is False:
        gene_signature.softfile.normalize = False
    else:
        gene_signature.softfile.normalize = True
    return gene_signature