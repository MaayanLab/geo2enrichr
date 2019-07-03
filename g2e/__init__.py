"""Configures the application at server startup.
"""

import logging
import sys

from flask import Flask, jsonify, session as flask_session
from flask_cors import CORS
from flask_login import LoginManager, user_logged_out

from substrate import User, db as substrate_db
from . import config
from .exceptions import AppException


app = Flask(__name__, static_url_path='/g2e/static', static_folder='static')


# User authentication and sessioning.
# ----------------------------------------------------------------------------
# Change this SECRET_KEY to force all users to re-authenticate.
app.secret_key = config.SECRET_KEY


@app.before_request
def make_session_permanent():
    """Sets Flask session to 'permanent', meaning 31 days.
    """
    flask_session.permanent = True


# Database configurations.
# ----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = config.SQLALCHEMY_POOL_RECYCLE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

substrate_db.init_app(app)


# Cross origin requests.
# ----------------------------------------------------------------------------
cors = CORS(app)

if not config.DEBUG:
    # Configure Apache logging.
    logging.basicConfig(stream=sys.stderr)
else:
    print('Starting in DEBUG mode')


# Setup endpoints (Flask Blueprints)
# ----------------------------------------------------------------------------
# Import these after connecting to the DB.
from . import endpoints

app.register_blueprint(endpoints.account_page)
app.register_blueprint(endpoints.auth_pages)
app.register_blueprint(endpoints.menu_pages)
app.register_blueprint(endpoints.results_page)
app.register_blueprint(endpoints.cluster_page)

app.register_blueprint(endpoints.check_duplicate_api)
app.register_blueprint(endpoints.extract_api)
app.register_blueprint(endpoints.gene_list_api)
app.register_blueprint(endpoints.pca_api)
app.register_blueprint(endpoints.soft_file_api)

app.register_blueprint(endpoints.jinjafilters)


# User authentication
# ----------------------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_pages.login'


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


# Error handling
# ----------------------------------------------------------------------------

# The order of registering these error handlers matters!

@app.errorhandler(AppException)
def handle_app_exceptions(error):
    """Custom error handling for application.
    """
    response = jsonify(error.serialize)
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def handle_any_exceptions(error):
    """Generic error handling.
    """
    import traceback
    print(traceback.format_exc())
    response = jsonify({
        'error': 'Unknown error. Please contact the Ma\'ayan Lab.',
        'python_error': str(error),
    })
    response.status_code = 500
    return response


# Setup global variables that are available in Jinja2 templates
# ----------------------------------------------------------------------------
app.config.update({
    'BASE_URL': config.BASE_URL,

    'API_URL': config.API_URL,
    'EXTRACT_URL': config.EXTRACT_URL,
    'PCA_URL': config.PCA_URL,
    'RESULTS_URL': config.RESULTS_URL,
    'SOFT_FILE_URL': config.SOFT_FILE_URL,
    'CLUSTER_URL': config.CLUSTER_URL,
    'GENE_LIST_URL': config.GENE_LIST_URL,

    'GEN3VA_URL': config.GEN3VA_URL,
    'GEN3VA_REPORT_URL': config.GEN3VA_REPORT_URL,
    'GEN3VA_TAG_URL': config.GEN3VA_TAG_URL
})
