"""creating soft file table

Revision ID: 28cc06993b73
Revises: 4d5f9ba76c5e
Create Date: 2015-08-27 12:08:52.581396

"""

# revision identifiers, used by Alembic.
revision = '28cc06993b73'
down_revision = '4d5f9ba76c5e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'soft_file_sample',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('soft_file_fk', sa.Integer),
        sa.Column('name', sa.String(255)),
        sa.Column('is_control', sa.Boolean)
    )
    op.create_foreign_key(None, 'soft_file_sample', 'soft_file', ['soft_file_fk'], ['id'])