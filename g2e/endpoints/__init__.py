"""Interface for endpoints module.
"""

from jinja_filters import jinjafilters

from pages.account_page import account_page
from pages.authentication_pages import auth_pages
from pages.cluster_page import cluster_page
from pages.menu_pages import menu_pages
from pages.results_page import results_page

from api.status_api import check_api
from api.extract_api import extract_api
from api.gene_list_api import gene_list_api
from api.pca_api import pca_api
from api.soft_file_api import soft_file_api
from api.upload_api import upload_api
