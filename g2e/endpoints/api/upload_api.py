"""API for uploading pre-existing gene signatures, i.e. does not perform
differential expression analysis.
"""

import json

from flask import Blueprint, request

from substrate import Gene, RankedGene
from g2e import config, database, signature_factory


upload_api = Blueprint('upload_api',
                       __name__,
                       url_prefix=config.UPLOAD_URL)


@upload_api.route('/', methods=['POST'])
def upload_gene_signature():
    """Uploads gene signature and returns extraction ID.
    """
    try:
        import pdb; pdb.set_trace()
        data = json.loads(request.data)
        ranked_genes = data['ranked_genes']
        gene_signature = signature_factory.from_gene_list(ranked_genes)
        return 'jr;;p'
    except:
        pass
