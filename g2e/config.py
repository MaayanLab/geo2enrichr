"""Handles all application configurations.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import os


class Config(object):

    with open('g2e/app.conf') as f:
        lines = [x for x in f.read().split('\n')]

    DEBUG = bool(lines[1])
    SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'

    BASE_URL = '/g2e'
    BASE_API_URL = BASE_URL + '/api'
    BASE_EXPLORE_URL = BASE_URL + '/explore'

    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_DATABASE_URI = lines[0]