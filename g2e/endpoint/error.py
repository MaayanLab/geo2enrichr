"""Error handling.
"""


from flask import Blueprint
from g2e.config import Config
from g2e import app
from flask import render_template


error = Blueprint('error', __name__, url_prefix=Config.BASE_URL)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')