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

from g2e.app.config import DEBUG, SQLALCHEMY_DATABASE_URI


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
cors = CORS(app)

if not DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)

# Import these after connecting to the DB.
from g2e.endpoint.index import index
from g2e.endpoint.static import static
from g2e.endpoint.api import api

app.register_blueprint(index)
app.register_blueprint(static)
app.register_blueprint(api)