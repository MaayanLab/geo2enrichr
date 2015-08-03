"""This module starts the g2e server.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

import sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from g2e.app.config import DEBUG
from g2e.endpoint.index import index
from g2e.endpoint.static import static
from g2e.endpoint.api import api


if not DEBUG:
    # Allows for logging data to Apache's logs.
    import logging
    logging.basicConfig(stream=sys.stderr)


app = Flask(__name__, static_url_path='')
db = SQLAlchemy(app)

app.register_blueprint(index)
app.register_blueprint(static)
app.register_blueprint(api)