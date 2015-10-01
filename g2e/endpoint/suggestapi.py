"""Returns keyword suggestions based on a prefix query.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from flask import Blueprint
import json
from g2e.config import Config
from g2e.dataaccess import dataaccess


suggest_api_blueprint = Blueprint('suggestapi', __name__, url_prefix=Config.BASE_API_URL + '/suggest')


@suggest_api_blueprint.route('')
@suggest_api_blueprint.route('/')
@suggest_api_blueprint.route('/<query>')
def fetch_suggestions(query=''):
    """Returns a list of suggestions based on a user query.
    """
    suggestions = dataaccess.get_suggestions(query)
    return json.dumps(suggestions)
