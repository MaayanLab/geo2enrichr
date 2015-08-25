"""Handles all API requests.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint
import jinja2
import urllib


jinjafilters = Blueprint('filters', __name__)


@jinja2.contextfilter
@jinjafilters.app_template_filter('custom_urlencode')
def custom_urlencode(context, value):
    return urllib.quote_plus(value)