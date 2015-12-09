"""Suggest API for autocomplete.
"""

from flask import Blueprint
import json

from g2e.db import dataaccess
from g2e.config import Config

suggest_api = Blueprint('suggest_api', __name__, url_prefix=Config.BASE_API_URL + '/suggest')


@suggest_api.route('')
@suggest_api.route('/')
@suggest_api.route('/<query>')
def suggest(query=''):
    """Returns a list of suggestions based on a user query.
    """
    suggestions = dataaccess.get_suggestions(query)
    return json.dumps(suggestions)
