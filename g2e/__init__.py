"""Configures the application at server startup.
"""

import logging
import sys

from flask import Flask
from flask.ext.cors import CORS
from g2e.config import Config
from substrate import db as substrate_db

app = Flask(__name__, static_url_path='/g2e/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = Config.SQLALCHEMY_POOL_RECYCLE

# My understanding is that track changes just uses up unnecessary resources
# and will be set to False by default in a future release of Flask-SQLAlchemy.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

substrate_db.init_app(app)
cors = CORS(app)

if not Config.DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)
else:
    print 'Starting in DEBUG mode'

# Import these after connecting to the DB.
from g2e import endpoints

app.register_blueprint(endpoints.menu_pages)
app.register_blueprint(endpoints.results_page)
app.register_blueprint(endpoints.cluster_page)

app.register_blueprint(endpoints.check_api)
app.register_blueprint(endpoints.extract_api)
app.register_blueprint(endpoints.gene_list_api)
app.register_blueprint(endpoints.pca_api)
app.register_blueprint(endpoints.soft_file_api)

app.register_blueprint(endpoints.jinjafilters)
