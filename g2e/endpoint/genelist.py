"""Builds a GeneList file upon request.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, Response
from g2e.config import BASE_URL
from g2e.dao import genelistdao
from g2e.core.genelist import filemaker


genelist = Blueprint('genelist', __name__, url_prefix=BASE_URL + '/genelist')


@genelist.route('/<genelist_name>')
def get_genelist(genelist_name):
    """Handle GET request based on extraction ID.
    """
    genelist = genelistdao.fetch(genelist_name)
    genelist_str = filemaker.get_file_contents_as_string(genelist)
    response = Response(genelist_str, mimetype='text/plain')
    #response.headers['Content-Disposition'] = 'attachment; filename=' + genelist_name + '.txt'
    return response