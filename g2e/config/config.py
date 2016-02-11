"""Global configurations.
"""

from ConfigParser import ConfigParser
import os


config = ConfigParser()

# g2e/config.ini is an un-version controlled config file.
#
# 'mode.debug' specifies the application debug mode.
# 'db.uri' specifies which database to connect to:
#    mysql://<USER>:<PASSWORD>@<IP ADDRESS>:<PORT | 3306>/<DB>
config.read('g2e/config/config.ini')

DEBUG = config.getboolean('mode', 'debug')
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/g2e/g2e'
SECRET_KEY = config.get('cookies', 'secret_key')
ADMIN_KEY = config.get('admin', 'admin_key')

BASE_URL = '/g2e'

RESULTS_URL = BASE_URL + '/results'
PCA_URL = BASE_URL + '/pca'
CLUSTER_URL = BASE_URL + '/cluster'

GENE_LIST_URL = BASE_URL + '/gene_list'
SOFT_FILE_URL = BASE_URL + '/soft_file'

API_URL = BASE_URL + '/api'
EXTRACT_URL = API_URL + '/extract'

SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_DATABASE_URI = config.get('db', 'uri')

if DEBUG:
    GEN3VA_URL = 'http://localhost:8084/gen3va'
    SERVER_URL = 'http://localhost:8083'
else:
    GEN3VA_URL = 'http://amp.pharm.mssm.edu/gen3va'
    SERVER_URL = 'http://amp.pharm.mssm.edu'

GEN3VA_REPORT_URL = GEN3VA_URL + '/report'
GEN3VA_TAG_URL = GEN3VA_URL + '/tag'
