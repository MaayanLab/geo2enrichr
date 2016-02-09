"""Handles user account page.
"""

from flask import Blueprint, render_template

from g2e import config


account_page = Blueprint('account_page',
                         __name__,
                         url_prefix=config.BASE_URL)


@account_page.route('/account', methods=['GET', 'POST'])
def view_account_page():
    return render_template('pages/account.html')
