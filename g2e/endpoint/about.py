"""Serves about page with statistics.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint, render_template
import json
from g2e.config import Config
from g2e.dataaccess import dataaccess


about = Blueprint('about', __name__, url_prefix=Config.BASE_URL)


@about.route('/about')
def about_page():
    stats = dataaccess.get_statistics()
    stats_json = json.dumps(stats)
    return render_template('about.html', stats=stats, stats_json=stats_json)
