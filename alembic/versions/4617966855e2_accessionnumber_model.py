"""AccessionNumber model

Revision ID: 4617966855e2
Revises: 1389749e3669
Create Date: 2015-10-27 17:36:17.119316

"""

# revision identifiers, used by Alembic.
revision = '4617966855e2'
down_revision = '1389749e3669'
branch_labels = None
depends_on = None

import json
import time

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import requests

from g2e.model.geodataset import GeoDataset
from g2e.model.customdataset import CustomDataset
from g2e.model.genesignature import GeneSignature


Session = sessionmaker()


def upgrade():

    # op.create_table(
    #     'dataset',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('title', sa.Text),
    #     sa.Column('record_type', sa.String(32), nullable=False),
    #     sa.Column('organism', sa.String(255)),
    #
    #     # GEO specific columns.
    #     sa.Column('accession', sa.String(255)),
    #     sa.Column('platform', sa.String(32)),
    #     sa.Column('summary', sa.Text)
    # )
    #
    # op.add_column('soft_file',
    #     sa.Column('dataset_fk', sa.Integer)
    # )
    #
    # op.create_foreign_key(None, 'soft_file', 'dataset', ['dataset_fk'], ['id'])

    # TODO:
    #op.drop_column('soft_file', 'is_geo')
    #op.drop_column('soft_file', 'name')
    #op.drop_column('soft_file', 'platform')

    #_create_accession_numbers()

    raise Exception('Don\'t finish!')


def _create_accession_numbers():
    """Create new data records for every extracted gene signature.
    """
    conn = op.get_bind()
    session = Session(bind=conn)
    for idx, sig in enumerate(session.query(GeneSignature)):
        if sig.soft_file.is_geo == 1:
            dataset_id = _load_geo_record(session, sig.soft_file)
        else:
            dataset_id = _load_custom(session, sig.soft_file)

        sig.soft_file.dataset_fk = dataset_id
        print '%s - %s' % (idx, sig.soft_file.name)
        session.commit()


def _load_geo_record(session, soft_file):
    data = _load_data_from_gds(session, soft_file)
    accession = soft_file.name
    platform = data['gpl'] if 'gpl' in data else soft_file.platform
    title = data['title'] if 'title' in data else None
    organism = data['taxon'] if 'taxon' in data else None
    return _get_or_create_geo_record(session, accession, title, platform, organism, None)


def _load_data_from_gds(session, soft_file):
    accession = soft_file.name
    http_session = requests.session()
    if 'GDS' in accession:
        url = _get_gds_url(accession[3:])
        response = http_session.get(url)
        acc_id = accession[3:]
        data = json.loads(response.text)['result'][acc_id]
    else:
        search_url = _get_gse_search_url(accession)
        response = http_session.get(search_url)
        search_data = json.loads(response.text)['esearchresult']
        acc_id = search_data['idlist'][0]
        url = _get_gds_url(acc_id)
        response = http_session.get(url)
        data = json.loads(response.text)['result'][acc_id]
    return data


# GEO API handlers
# --------------

BASE_GEO_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/%s.fcgi?&retmax=1&retmode=json&db=gds'


def _get_gds_url(acc_id):
    url = BASE_GEO_URL % 'esummary'
    return url + '&id=' + acc_id


def _get_gse_search_url(acc_full):
    url = BASE_GEO_URL % 'esearch'
    return url + '&term=' + acc_full


# Data accessors
# --------------

def _get_or_create_geo_record(session, accession, title, platform, organism, summary):
    instance = session.query(GeoDataset).filter_by(accession=accession).first()
    if not instance:
        instance = GeoDataset(
            accession=accession,
            title=title,
            platform=platform,
            organism=organism,
            summary=summary
        )
        session.add(instance)
        session.flush()
        session.refresh(instance)
        return instance.id
    return instance.id


def _load_custom(session, soft_file):
    title = soft_file.name
    instance = CustomDataset(
        title=title
    )
    session.add(instance)
    session.flush()
    return instance.id



# def _transfer_data():
#
#     conn = op.get_bind()
#     session = Session(bind=conn)
#
#     an_tbl = AccessionNumber.__table__
#     gs_tbl = GeneSignature.__table__
#
#     for sig in session.query(GeneSignature):
#         is_geo = sig.soft_file.is_geo == 1
#         if is_geo:
#             geo_id = sig.soft_file.name

    # sql = 'SELECT gene_signature.id, soft_file.name, soft_file.is_geo ' \
    #       '  FROM gene_signature ' \
    #       'JOIN soft_file ON soft_file.gene_signature_fk = gene_signature.id'

    # results = conn.execute(sql).fetchall()
    #
    # data_to_transfer = []
    # for r in results:
    #     gene_signature_id = r[0]
    #     name = r[1]
    #     is_geo = r[2]
    #     if is_geo == 1:
    #         data_to_transfer.append({
    #             'geo_id': name
    #         })
    #
    # op.bulk_insert(an_tbl, data_to_transfer)

    # data_to_transfer = []
    # idx_to_fk = [None, 1, 2, 3]
    # for r in results:
    #     for i in [1,2,3]:
    #         if _is_not_empty(r[i]):
    #             data_to_transfer.append({
    #                 'target_app_fk': idx_to_fk[i],
    #                 'gene_list_fk': r[0],
    #                 'link': r[i]
    #             })
    #
    # # I get a connection timeout when I try to bulk insert all the data.
    # cutoff = int(round(len(data_to_transfer) / 2))
    # data_to_transfer1 = data_to_transfer[:cutoff]
    # data_to_transfer2 = data_to_transfer[cutoff:]
    # op.bulk_insert(link_tbl, data_to_transfer1)
    # op.bulk_insert(link_tbl, data_to_transfer2)


if __name__ == '__main__':
    upgrade()
