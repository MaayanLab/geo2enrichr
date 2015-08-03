"""Serves static files.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, send_from_directory

from g2e.app.config import BASE_URL, SERVER_ROOT


static = Blueprint('static', __name__, url_prefix=BASE_URL + '/<path:path>')


@static.route('/')
def static_endpoint(path):
    return send_from_directory(SERVER_ROOT, path)