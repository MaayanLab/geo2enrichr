"""API for uploading pre-existing gene signatures.
"""

import json

from flask import Blueprint, request

from substrate import Gene, GeneSignature, RankedGene
from g2e import config, db


upload_api = Blueprint('upload_api',
                       __name__,
                       url_prefix=config.UPLOAD_URL)


@upload_api.route('/', methods=['POST'])
def upload_gene_signature():
    """
    """
    try:
        data = json.loads(request.data)
        gene_signature = GeneSignature()
        for rg in data['ranked_genes']:
            symbol = rg[0]
            value = rg[1]
            gene = db.get_or_create(Gene, name=symbol)
            ranked_gene = RankedGene(gene, value)
            print(ranked_gene)
        return 'jr;;p'
    except:
        pass
