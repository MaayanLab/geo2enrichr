"""Error handling.
"""

from g2e import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')
