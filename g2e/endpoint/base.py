"""Serves home page.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
from g2e.config import Config


base = Blueprint('base', __name__, url_prefix=Config.BASE_URL)


@base.route('/')
def index_page():
    return render_template('index.html')


@base.route('/documentation')
def documentation_page():
    return render_template('documentation.html')


@base.route('/manual')
def manual_page():
    return render_template('manual.html')


@base.route('/pipeline')
def pipeline_page():
    return render_template('pipeline.html')