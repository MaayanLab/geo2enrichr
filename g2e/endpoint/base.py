"""Serves home page.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
import json
from g2e.config import Config
from g2e.dataaccess import dataaccess


base = Blueprint('base', __name__, url_prefix=Config.BASE_URL)


@base.route('/')
def index_page():
    stats = dataaccess.get_statistics()
    stats_json = json.dumps(stats)
    return render_template('index.html', stats=stats, stats_json=stats_json)


@base.route('/documentation')
def documentation_page():
    return render_template('documentation.html')


@base.route('/manual')
def manual_page():
    return render_template('manual.html')


@base.route('/pipeline')
def pipeline_page():
    return render_template('pipeline.html')


@base.route('/stats')
def stats_page():
    stats = dataaccess.get_statistics()
    stats_json = json.dumps(stats)
    return render_template('stats.html', stats=stats, stats_json=stats_json)


@base.route('/about')
def about_page():
    return render_template('about.html')