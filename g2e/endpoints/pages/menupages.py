"""Serves home page and miscellaneous pages.
"""

from flask import Blueprint, render_template

from g2e.config import Config
from g2e import db

menu_pages = Blueprint('base',
                       __name__,
                       url_prefix=Config.BASE_URL)


@menu_pages.route('/')
def index_page():
    num_gene_signatures = db.get_num_gene_signatures()
    return render_template('index.html',
                           num_gene_signatures=num_gene_signatures)


@menu_pages.route('/documentation')
def documentation_page():
    return render_template('pages/documentation.html')


@menu_pages.route('/manual')
def manual_page():
    return render_template('pages/manual.html')


@menu_pages.route('/pipeline')
def pipeline_page():
    return render_template('pages/pipeline.html')


@menu_pages.route('/about')
def about_page():
    return render_template('pages/about.html')
