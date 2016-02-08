"""Interface for endpoints module.
"""

from jinjafilters import jinjafilters

from pages.accountpage import account_page
from pages.authpages import auth_pages
from pages.clusterpage import cluster_page
from pages.menupages import menu_pages
from pages.resultspage import results_page

from api.checkapi import check_api
from api.extractapi import extract_api
from api.genelistapi import gene_list_api
from api.pcaapi import pca_api
from api.softfileapi import soft_file_api
from api.uploadapi import upload_api
