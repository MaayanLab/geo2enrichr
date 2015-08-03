"""Handles all application configurations.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os


DEBUG = False
BASE_URL = '/g2e'
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'

with open('g2e/orm/db.conf') as f:
    SQLALCHEMY_DATABASE_URI = f.read().strip()