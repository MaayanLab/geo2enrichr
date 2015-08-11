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
else:
    print 'Starting in DEBUG mode'

# Import these after connecting to the DB.
from g2e.endpoint.base import base
from g2e.endpoint.error import error
from g2e.endpoint.static import static
from g2e.endpoint.extract import extract
from g2e.endpoint.tag import tag

app.register_blueprint(base)
app.register_blueprint(error)
app.register_blueprint(static)
app.register_blueprint(extract)
app.register_blueprint(tag)