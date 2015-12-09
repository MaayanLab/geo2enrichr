"""Global configurations.
"""

import os


class Config(object):
    """Global configurations.
    """

    # g2e/app.conf un-version controlled, two-line file.
    #
    # First line - DB connection:
    #   mysql://<USER>:<PASSWORD>@<IP ADDRESS>:<PORT | 3306>/<DB>
    #
    # Second line - DEBUG mode:
    #   True | False
    with open('g2e/app.conf') as f:
        lines = [x for x in f.read().split('\n')]

    DEBUG = lines[1] == 'True'
    SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'

    BASE_URL = '/g2e'

    RESULTS_PAGE_URL = BASE_URL + '/results'
    BASE_API_URL = BASE_URL + '/api'
    BASE_PCA_URL = BASE_URL + '/pca'
    BASE_CLUSTER_URL = BASE_URL + '/cluster'

    GENE_LIST_URL = BASE_URL + '/gene_list'
    SOFT_FILE_URL = BASE_URL + '/soft_file'
    SUGGEST_API = BASE_URL + '/suggest'

    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_DATABASE_URI = lines[0]

    if DEBUG:
        GENEVA_URL = 'http://localhost:8084/geneva'
    else:
        GENEVA_URL = 'http://amp.pharm.mssm.edu/geneva'

    GENEVA_REPORT_URL = GENEVA_URL + '/report'
    GENEVA_METADATA_URL = GENEVA_URL + '/metadata'
