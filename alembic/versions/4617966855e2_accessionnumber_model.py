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


# 5174 - GSE63415 - bb32c4fa32


def upgrade():

    op.create_table(
        'dataset',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Text),
        sa.Column('record_type', sa.String(32), nullable=False),
        sa.Column('organism', sa.String(255)),

        # GEO specific columns.
        sa.Column('accession', sa.String(255)),
        sa.Column('platform', sa.String(32)),
        sa.Column('summary', sa.Text)
    )

    op.add_column('soft_file',
        sa.Column('dataset_fk', sa.Integer)
    )

    op.create_foreign_key(None, 'soft_file', 'dataset', ['dataset_fk'], ['id'])
    _create_accession_numbers()


def _create_accession_numbers():
    """Create new data records for every extracted gene signature.
    """
    conn = op.get_bind()
    session = Session(bind=conn)
    with open('log.txt', 'w+') as error_log:
        for idx, sig in enumerate(session.query(GeneSignature)):
            msg = '%s - %s - %s' % (idx, sig.soft_file.name, sig.extraction_id)
            print msg
            try:
                if sig.soft_file.is_geo == 1:
                    dataset_id = _load_geo_record(session, sig.soft_file)
                else:
                    dataset_id = _load_custom(session, sig.soft_file)
            except:
                error_log.write(msg)

            sig.soft_file.dataset_fk = dataset_id
            session.commit()


def _load_geo_record(session, soft_file):
    data = _load_data_from_gds(soft_file)
    accession = soft_file.name
    title = data['title'] if 'title' in data else None
    summary = data['summary'] if 'summary' in data else None
    platform = data['gpl'] if 'gpl' in data else soft_file.platform
    organism = data['taxon'] if 'taxon' in data else None
    return _get_or_create_geo_record(session, accession, title, summary, platform, organism)


def _load_data_from_gds(soft_file):
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

def _get_or_create_geo_record(session, accession, title, summary, platform, organism):
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
