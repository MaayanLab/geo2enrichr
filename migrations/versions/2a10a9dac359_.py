"""empty message

Revision ID: 2a10a9dac359
Revises: 1195f491e402
Create Date: 2015-08-10 18:00:24.566632

"""

# revision identifiers, used by Alembic.
revision = '2a10a9dac359'
down_revision = '1195f491e402'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('metadata_tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags_to_extractions',
        sa.Column('extraction_fk', sa.Integer(), nullable=True),
        sa.Column('metadata_tag_fk', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['extraction_fk'], ['extractions.id'], ),
        sa.ForeignKeyConstraint(['metadata_tag_fk'], ['metadata_tag.id'], )
    )


def downgrade():
    op.drop_table('tags_to_extractions')
    op.drop_table('metadata_tag')
