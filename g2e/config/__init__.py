"""Interface for config module. Designed to be convertable to a dict and then
mixed into Flask's config object.
"""

from .config import \
    \
    DEBUG, \
    SERVER_ROOT, \
    SECRET_KEY, \
    SERVER_URL, \
    ADMIN_KEY, \
    \
    BASE_URL, \
    \
    API_URL, \
    EXTRACT_URL, \
    \
    PCA_URL, \
    CLUSTER_URL, \
    RESULTS_URL, \
    GENE_LIST_URL, \
    SOFT_FILE_URL, \
    \
    GEN3VA_URL, \
    GEN3VA_REPORT_URL, \
    GEN3VA_TAG_URL, \
    \
    SQLALCHEMY_DATABASE_URI, \
    SQLALCHEMY_POOL_RECYCLE
