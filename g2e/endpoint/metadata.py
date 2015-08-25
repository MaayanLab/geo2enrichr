"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
from g2e.config import Config
import g2e.dataaccess.dataaccess as dataaccess


metadata = Blueprint('metadata', __name__, url_prefix=Config.BASE_EXPLORE_URL + '/metadata')


@metadata.route('/<path:metadata_name>', methods=['GET'])
def metadata_endpoint(metadata_name):
    metadata = dataaccess.fetch_metadata(metadata_name)
    if metadata is None:
        return render_template('not-found.html',
            message='No gene signatures with metadata "%s" found' % metadata_name
        )
    else:
        return render_template('metadata.html',
            results_url=Config.BASE_URL + '/results',
            tag_url=Config.BASE_URL + '/explore/tag',
            metadata_url=Config.BASE_URL + '/explore/metadata',
            metadata=metadata
        )


@metadata.route('/<path:metadata_name>/<path:metadata_value>', methods=['GET'])
def metadata_with_value_endpoint(metadata_name, metadata_value):
    metadata = dataaccess.fetch_metadata_by_value(metadata_name, metadata_value)
    print metadata_value
    if metadata is None or len(metadata) == 0:
        return render_template('not-found.html',
            message='No gene signatures with metadata "%s" found' % metadata_name
        )
    else:
        return render_template('metadata-by-value.html',
            metadata_name=metadata_name,
            results_url=Config.BASE_URL + '/results',
            tag_url=Config.BASE_URL + '/explore/tag',
            metadata=metadata
        )