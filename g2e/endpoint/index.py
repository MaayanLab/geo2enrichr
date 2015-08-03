"""Serves home page.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint
from g2e.app.config import BASE_URL, SERVER_ROOT
from flask import send_from_directory


index = Blueprint('index', __name__, url_prefix=BASE_URL + '/')


@index.route('/')
def index_point():
    return send_from_directory(SERVER_ROOT + '/web/site', 'index.html')