"""Added column to soft_file table for text file blob

Revision ID: 3da6bc91d6c1
Revises: 28cc06993b73
Create Date: 2015-09-04 14:53:03.246163

"""

# revision identifiers, used by Alembic.
revision = '3da6bc91d6c1'
down_revision = '28cc06993b73'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('soft_file', sa.Column('actual_text_file', sa.LargeBinary))