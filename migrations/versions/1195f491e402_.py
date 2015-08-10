"""empty message

Revision ID: 1195f491e402
Revises: None
Create Date: 2015-08-10 13:08:07.506075

"""

# revision identifiers, used by Alembic.
revision = '1195f491e402'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    metadata_tbl = op.create_table('exp_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_fk', sa.Integer(), nullable=True),
        sa.Column('diff_exp_method_fk', sa.Integer(), nullable=True),
        sa.Column('ttest_correction_method_fk', sa.Integer(), nullable=True),
        sa.Column('cutoff', sa.Integer(), nullable=True),
        sa.Column('threshold', sa.Float(), nullable=True),
        sa.Column('organism', sa.String(length=255), nullable=True),
        sa.Column('cell', sa.String(length=255), nullable=True),
        sa.Column('perturbation', sa.String(length=255), nullable=True),
        sa.Column('gene', sa.String(length=255), nullable=True),
        sa.Column('disease', sa.String(length=255), nullable=True),
        sa.Column('platform', sa.String(length=255), nullable=True),
        sa.Column('normalize', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['diff_exp_method_fk'], ['diff_exp_method.id'], ),
        sa.ForeignKeyConstraint(['extraction_fk'], ['extractions.id'], ),
        sa.ForeignKeyConstraint(['ttest_correction_method_fk'], ['ttest_correction_method.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Manually update the DB.
    conn = op.get_bind()
    res = conn.execute("SELECT id, diff_exp_method_fk, cutoff, ttest_correction_method_fk, threshold, organism, cell, perturbation, gene, disease FROM extractions")
    results = res.fetchall()
    metadata_rows = [
        {
            'extraction_fk': r[0],
            'diff_exp_method_fk': r[1],
            'cutoff': r[2],
            'ttest_correction_method_fk': r[3],
            'threshold': r[4],
            'organism': r[5],
            'cell': r[6],
            'perturbation': r[7],
            'gene': r[8],
            'disease': r[9],
        } for r in results

    ]
    op.bulk_insert(metadata_tbl, metadata_rows)

    op.drop_constraint(u'extractions_ibfk_1', 'extractions', type_='foreignkey')
    op.drop_constraint(u'extractions_ibfk_2', 'extractions', type_='foreignkey')
    op.drop_column(u'extractions', 'cutoff')
    op.drop_column(u'extractions', 'perturbation')
    op.drop_column(u'extractions', 'diff_exp_method_fk')
    op.drop_column(u'extractions', 'ttest_correction_method_fk')
    op.drop_column(u'extractions', 'disease')
    op.drop_column(u'extractions', 'cell')
    op.drop_column(u'extractions', 'threshold')
    op.drop_column(u'extractions', 'gene')
    op.drop_column(u'extractions', 'organism')
    op.drop_column(u'rankedgenes', 'value_type')

    # Alembic is generating this, but I'm not sure why.
    #op.drop_index('extraction_id', table_name='softfiles')

    op.alter_column(u'diff_exp_method', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column(u'ttest_correction_method', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)