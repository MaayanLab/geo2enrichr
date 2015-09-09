"""Remove unneeded gene_list.text_file

Revision ID: 1389749e3669
Revises: 4891a6138506
Create Date: 2015-09-09 18:31:18.735166

"""

# revision identifiers, used by Alembic.
revision = '1389749e3669'
down_revision = '4891a6138506'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('gene_list', 'text_file')