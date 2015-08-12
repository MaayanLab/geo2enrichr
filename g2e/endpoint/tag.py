"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
from g2e.app.config import BASE_URL
import g2e.dao.tagdao as tagdao


tag = Blueprint('tag', __name__, url_prefix=BASE_URL + '/tag')


@tag.route('/<tag_name>', methods=['GET'])
def tag_endpoint(tag_name):
    tag = tagdao.fetch(tag_name)

    return render_template('tag.html',
        base_url=BASE_URL + '/results',
        num_tags=len(tag.extractions),
        tag=tag
    )