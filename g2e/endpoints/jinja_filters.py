"""Custom filters for Jinja2 templates.
"""

from flask import Blueprint
import jinja2


jinjafilters = Blueprint('filters', __name__)


# Data filters
# ----------------------------------------------------------------------------
@jinja2.contextfilter
@jinjafilters.app_template_filter('c_filter_optional_metadata')
def c_filter_optional_metadata(context, value):
    results = []
    for metadata in value:
        if (
            metadata.value == None or
            metadata.value.strip() == '' or
            metadata.name == 'user_key' or
            metadata.name == 'userKey' or
            metadata.name == 'userEmail' or
            metadata.name == 'user_email'
        ):
            continue
        results.append(metadata)
    return results


# URL builders
# ----------------------------------------------------------------------------
@jinja2.contextfilter
@jinjafilters.app_template_filter('c_geo_url')
def c_geo_url(context, value):
    if 'GDS' in value:
        return 'http://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=' + value
    return 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + value
