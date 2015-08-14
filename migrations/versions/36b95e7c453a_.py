"""empty message

Revision ID: 36b95e7c453a
Revises: 2a10a9dac359
Create Date: 2015-08-14 12:18:03.502676

"""

# revision identifiers, used by Alembic.
revision = '36b95e7c453a'
down_revision = '2a10a9dac359'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.drop_column('genelists', 'name')


def downgrade():
    op.add_column('genelists', sa.Column('name', mysql.VARCHAR(length=200), nullable=True))
