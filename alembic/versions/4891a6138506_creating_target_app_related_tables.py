"""Creating target_app related tables

Revision ID: 4891a6138506
Revises: 3da6bc91d6c1
Create Date: 2015-09-08 18:15:28.631133

"""

# revision identifiers, used by Alembic.
revision = '4891a6138506'
down_revision = '3da6bc91d6c1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    #_build_target_app()
    link_tbl = _build_target_app_link()
    _transfer_data(link_tbl)
    raise Exception('whatever')


def _build_target_app():
    tbl = op.create_table(
        'target_app',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
    )
    apps = [
        {'name': 'enrichr'},
        {'name': 'l1000cds2'},
        {'name': 'paea'},
        {'name': 'crowdsourcing'}
    ]
    op.bulk_insert(tbl, apps)


def _build_target_app_link():
    link_tbl = op.create_table(
        'target_app_link',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('target_app_fk', sa.Integer),
        sa.Column('gene_list_fk', sa.Integer),
        sa.Column('link', sa.Text)
    )
    op.create_foreign_key(None, 'target_app_link', 'target_app', ['target_app_fk'], ['id'])
    op.create_foreign_key(None, 'target_app_link', 'gene_list', ['gene_list_fk'], ['id'])
    return link_tbl


def _transfer_data(link_tbl):
    conn = op.get_bind()
    sql = 'SELECT id, enrichr_link, l1000cds2_link, paea_link FROM gene_list'
    results = conn.execute(sql).fetchall()

    data_to_transfer = []
    idx_to_fk = [None, 1, 2, 3]
    for r in results:
        for i in [1,2,3]:
            if _is_not_empty(r[i]):
                data_to_transfer.append({
                    'target_app_fk': idx_to_fk[i],
                    'gene_list_fk': r[0],
                    'link': r[i]
                })

    # I get a connection timeout when I try to bulk insert all the data.
    cutoff = int(round(len(data_to_transfer) / 2))
    data_to_transfer1 = data_to_transfer[:cutoff]
    data_to_transfer2 = data_to_transfer[cutoff:]
    op.bulk_insert(link_tbl, data_to_transfer1)
    op.bulk_insert(link_tbl, data_to_transfer2)


def _is_not_empty(link):
    return link is not None and link != ''


def downgrade():
    pass