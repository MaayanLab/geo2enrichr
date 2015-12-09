"""Configures the application at server startup.
"""

import logging
import sys

from flask import Flask
from flask.ext.cors import CORS

from g2e.config import Config
from substrate import db

app = Flask(__name__, static_url_path='/g2e/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = Config.SQLALCHEMY_POOL_RECYCLE

# My understanding is that track changes just uses up unnecessary resources
# and will be set to False by default in a future release of Flask-SQLAlchemy.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors = CORS(app)

if not Config.DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)
else:
    print 'Starting in DEBUG mode'

# Import these after connecting to the DB.
from g2e.endpoint.base import base
from g2e.endpoint.error import error
from g2e.endpoint.extractapi import extract_api
from g2e.endpoint.genelistapi import genelist
from g2e.endpoint.pcaapi import pca_blueprint
from g2e.endpoint.clusterapi import cluster_blueprint
from g2e.endpoint.softfile import soft_file
from g2e.endpoint.results import results
from g2e.endpoint.suggestapi import suggest_api_blueprint
from g2e.util.jinjafilters import jinjafilters

app.register_blueprint(base)
app.register_blueprint(cluster_blueprint)
app.register_blueprint(error)
app.register_blueprint(extract_api)
app.register_blueprint(genelist)
app.register_blueprint(pca_blueprint)
app.register_blueprint(soft_file)
app.register_blueprint(results)
app.register_blueprint(suggest_api_blueprint)
app.register_blueprint(jinjafilters)
