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
    extraction = dataaccess.fetch_extraction(results_id)
    if extraction is None:
        return render_template('404.html')

    extraction = __process_extraction_for_view(extraction)

    return render_template('results.html',
        use_simple_header=True,
        permanent_link=request.url,
        extraction=extraction
    )


def __get_direction_as_string(direction):
    if direction == 1:
        return 'Up'
    elif direction == -1:
        return 'Down'
    else:
        return 'Combined'


def __process_extraction_for_view(extraction):
    for gene_list in extraction.genelists:
        gene_list.direction_as_string = __get_direction_as_string(gene_list.direction)

    if extraction.exp_metadata.normalize is None or extraction.exp_metadata.normalize is False:
        extraction.exp_metadata.normalize = False
    else:
        extraction.exp_metadata.normalize = True
    return extraction