"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
from g2e.config import Config
import g2e.dataaccess.dataaccess as dataaccess


tag = Blueprint('tag', __name__, url_prefix=Config.BASE_URL + '/tag')


@tag.route('/<tag_name>', methods=['GET'])
def tag_endpoint(tag_name):
    tag = dataaccess.fetch_metadata_tag(tag_name)
    if tag is None:
        return render_template('not-found.html',
            message='No gene signatures with tag "%s" found' % tag_name
        )
    else:
        return render_template('tag.html',
            base_url=Config.BASE_URL + '/results',
            num_tags=len(tag.gene_signatures),
            tag=tag
        )