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

import requests
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from g2e.model.georecord import GeoRecord
from g2e.model.geodataset import GeoDataset
from g2e.model.geoprofile import GeoProfile
from g2e.model.genesignature import GeneSignature


Session = sessionmaker()


def upgrade():

    # op.create_table(
    #     'geo_record',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('accession', sa.String(255), nullable=False),
    #     sa.Column('record_type', sa.String(32), nullable=False),
    #     sa.Column('title', sa.String(255)),
    #     sa.Column('summary', sa.Text)
    # )
    #
    # op.add_column('soft_file',
    #     sa.Column('geo_record_fk', sa.Integer)
    # )
    #
    # op.create_foreign_key(None, 'soft_file', 'geo_record', ['geo_record_fk'], ['id'])
    _create_accession_numbers()

    raise Exception('Don\'t finish!')


def _create_accession_numbers():

    conn = op.get_bind()
    session = Session(bind=conn)

    for sig in session.query(GeneSignature):
        is_geo = sig.soft_file.is_geo == 1
        if is_geo:
            accession = sig.soft_file.name
            if 'GDS' in accession:
                _load(session, accession, True)
            else:
                _load(session, accession, False)



def _load(session, accession, is_gds):
    url = _get_url(accession)
    http_session = requests.session()
    response = http_session.get(url)
    if response.ok:
        acc_id = accession[3:]
        data = json.loads(response.text)['result'][acc_id]
        title = data['title']
        if is_gds:
            summary = data['summary']
            _get_or_create_gds(session, accession, title, summary)
        else:
            _get_or_create_gse(session, accession, title)


def _get_or_create_gds(session, accession, title, summary):
    instance = session.query(GeoRecord).filter_by(accession=accession).first()
    if not instance:
        print accession
        instance = GeoDataset(
            accession=accession,
            title=title,
            summary=summary,
            record_type='dataset'
        )
        session.add(instance)
        session.commit()


def _get_or_create_gse(session, accession, title):
    instance = session.query(GeoRecord).filter_by(accession=accession).first()
    if not instance:
        print accession
        instance = GeoProfile(
            accession=accession,
            title=title,
            record_type='profile'
        )
        session.add(instance)
        session.commit()


def _get_url(accession):
    is_gds = 'GDS' in accession
    BASE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?&retmax=1&retmode=json'
    db = 'gds' if is_gds else 'geoprofiles'
    return '&'.join([BASE_URL, 'db=' + db, 'id=' + accession[3:]])


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