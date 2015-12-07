"""Returns keyword suggestions based on a prefix query.
"""


from flask import Blueprint
import json

from g2e.db import dataaccess
from g2e.config import Config


suggest_api_blueprint = Blueprint('suggestapi', __name__, url_prefix=Config.BASE_API_URL + '/suggest')


@suggest_api_blueprint.route('')
@suggest_api_blueprint.route('/')
@suggest_api_blueprint.route('/<query>')
def fetch_suggestions(query=''):
    """Returns a list of suggestions based on a user query.
    """
    suggestions = dataaccess.get_suggestions(query)
    return json.dumps(suggestions)
