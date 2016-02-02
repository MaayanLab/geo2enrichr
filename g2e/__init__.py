"""Configures the application at server startup.
"""

import logging
import sys

from flask import Flask, session as flask_session
from flask.ext.cors import CORS
from flask.ext.login import LoginManager, user_logged_out

from substrate import User, db as substrate_db
from g2e import config


app = Flask(__name__, static_url_path='/g2e/static', static_folder='static')

# Cookies for user login sessions.
app.secret_key = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = config.SQLALCHEMY_POOL_RECYCLE

# My understanding is that track changes just uses up unnecessary resources
# and will be set to False by default in a future release of Flask-SQLAlchemy.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

substrate_db.init_app(app)
cors = CORS(app)

if not config.DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)
else:
    print 'Starting in DEBUG mode'

# Import these after connecting to the DB.
from g2e import endpoints

app.register_blueprint(endpoints.account_page)
app.register_blueprint(endpoints.auth_pages)
app.register_blueprint(endpoints.menu_pages)
app.register_blueprint(endpoints.results_page)
app.register_blueprint(endpoints.cluster_page)

app.register_blueprint(endpoints.check_api)
app.register_blueprint(endpoints.extract_api)
app.register_blueprint(endpoints.gene_list_api)
app.register_blueprint(endpoints.pca_api)
app.register_blueprint(endpoints.soft_file_api)

app.register_blueprint(endpoints.jinjafilters)


# User authentication
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'auth_pages.login'


@login_manager.user_loader
def load_user(user_id):
    """Utility method for loading User for Flask-Login.
    """
    user = substrate_db.session.query(User).get(user_id)
    app.config.user = user
    return user


@user_logged_out.connect_via(app)
def unset_current_user(sender, user):
    """When the user logs out, we need to unset this global variable.
    """
    app.config.user = None


@app.before_request
def make_session_permanent():
    """Sets Flask session to 'permanent', meaning 31 days.
    """
    flask_session.permanent = True
