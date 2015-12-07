"""Handles explore metadata pages.
"""


from flask import Blueprint, render_template

from g2e.config import Config
import g2e.db.dataaccess as dataaccess
import g2e.util.urlcodex as urlcodex


explore_metadata = Blueprint('explore_metadata', __name__, url_prefix=Config.BASE_METADATA_URL)


@explore_metadata.route('/<path:metadata_name>', methods=['GET'])
def metadata_endpoint(metadata_name):
    if metadata_name[-1] == '/':
        metadata_name = metadata_name[:-1]

    metadata_name = urlcodex.decode(metadata_name)
    metadata = dataaccess.fetch_metadata(metadata_name)
    if metadata is None:
        return render_template(
            '404.html',
            message='No gene signatures with metadata "%s" found' % metadata_name
        )
    else:
        return render_template(
            'metadata.html',
            metadata_name=metadata_name,
            results_url=Config.BASE_RESULTS_URL,
            tag_url=Config.BASE_TAGS_URL,
            metadata_url=Config.BASE_METADATA_URL,
            metadata=metadata
        )


@explore_metadata.route('/<path:metadata_name>/<path:metadata_value>', methods=['GET'])
def metadata_with_value_endpoint(metadata_name, metadata_value):
    metadata_name = urlcodex.decode(metadata_name)
    metadata_value = urlcodex.decode(metadata_value)
    metadata = dataaccess.fetch_metadata_by_value(metadata_name, metadata_value)
    if metadata is None or len(metadata) == 0:
        return render_template(
            '404.html',
            message='No gene signatures with metadata "%s" found' % metadata_name
        )
    else:
        return render_template(
            'metadata.html',
            metadata_name=metadata_name,
            metadata_value=metadata_value,
            results_url=Config.BASE_RESULTS_URL,
            tag_url=Config.BASE_TAGS_URL,
            metadata=metadata
        )
