"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
from g2e.config import Config
from g2e.model.tag import Tag
import g2e.dataaccess.dataaccess as dataaccess


explore_tags = Blueprint('explore_tags', __name__, url_prefix=Config.BASE_TAGS_URL)


@explore_tags.route('/', methods=['GET'])
def tags_endpoint():
    tags = dataaccess.fetch_all(Tag)
    return render_template('tags-all.html',
        num_tags=len(tags),
        tags=tags
    )


@explore_tags.route('/<tag_name>', methods=['GET'])
def tag_endpoint(tag_name):
    tag = dataaccess.fetch_tag(tag_name)
    if tag is None:
        return render_template('404.html',
            message='No gene signatures with tag "%s" found' % tag_name
        )
    else:
        return render_template('tag.html',
            num_tags=len(tag.gene_signatures),
            tag=tag
        )