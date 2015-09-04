"""This module starts the g2e server.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import logging
import sys

from flask import Flask
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
from g2e.util.jinjafilters import custom_urlencode

from g2e.config import Config


app = Flask(__name__, static_url_path='/g2e/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = Config.SQLALCHEMY_POOL_RECYCLE
db = SQLAlchemy(app)
cors = CORS(app)
app.jinja_env.filters['custom_urlencode'] = custom_urlencode

if not Config.DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)
else:
    print 'Starting in DEBUG mode'

# Import these after connecting to the DB.
from g2e.endpoint.base import base
from g2e.endpoint.error import error
from g2e.endpoint.exploremetadata import explore_metadata
from g2e.endpoint.exploretags import explore_tags
from g2e.endpoint.extractapi import extract_api
from g2e.endpoint.genelist import genelist
from g2e.endpoint.softfile import soft_file
from g2e.endpoint.results import results
from g2e.util.jinjafilters import jinjafilters

app.register_blueprint(base)
app.register_blueprint(error)
app.register_blueprint(extract_api)
app.register_blueprint(genelist)
app.register_blueprint(soft_file)
app.register_blueprint(explore_metadata)
app.register_blueprint(explore_tags)
app.register_blueprint(results)
app.register_blueprint(jinjafilters)