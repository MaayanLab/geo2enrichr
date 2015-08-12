"""Serves static files.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, make_response, send_from_directory

from g2e.config import BASE_URL, SERVER_ROOT


static = Blueprint('static', __name__, url_prefix=BASE_URL + '/static')

SOFTFILE_DIRECTORY = SERVER_ROOT + '/static/softfile/clean'
GENELIST_DIRECTORY = SERVER_ROOT + '/static/genelist'


# TODO: These should just return binary blogs from the DB, rather than
# referencing files on the hard disk.
@static.route('/softfile/clean/<filename>')
def softfile_download(filename):
    return send_from_directory(SOFTFILE_DIRECTORY, filename)


@static.route('/genelist/<filename>')
def genelist_download(filename):
    return send_from_directory(GENELIST_DIRECTORY, filename)