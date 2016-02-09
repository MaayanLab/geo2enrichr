"""API for hierarchical clustering.
"""

from flask import Blueprint, render_template
from g2e import config, database
from g2e.target_applications import clustergrammer


cluster_page = Blueprint('cluster_api',
                        __name__,
                        url_prefix='%s/cluster' % config.BASE_URL)


@cluster_page.route('/<extraction_id>', methods=['GET'])
def perform_hierarchical_clustering(extraction_id):
    """Performs hierarchical clustering on a SOFT file.
    """
    gene_signature = database.get_gene_signature(extraction_id)
    link = clustergrammer.from_soft_file(gene_signature)
    link = link + '&preview=true'
    return render_template('pages/clustergrammer.html',
                           clustergrammer_link=link,
                           results_url=config.RESULTS_URL,
                           extraction_id=gene_signature.extraction_id)
