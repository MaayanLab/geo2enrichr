"""Handles all application configurations.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os


DEBUG = True
BASE_URL = '/g2e'
BASE_API_URL = BASE_URL + '/api'
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'

with open('g2e/app/db.conf') as f:
    SQLALCHEMY_DATABASE_URI = f.read().strip()