"""Init

Revision ID: 48957fdfe8d5
Revises: 
Create Date: 2015-08-14 18:24:59.369915

"""

# revision identifiers, used by Alembic.
revision = '48957fdfe8d5'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    # rename tables
    # -------------
    op.rename_table('extractions', 'gene_signature')
    op.rename_table('softfiles', 'soft_file')
    op.rename_table('genelists', 'gene_list')
    op.rename_table('genes', 'gene')
    op.rename_table('rankedgenes', 'ranked_gene')
    op.rename_table('rankedgene2genelist', 'ranked_gene_2_gene_list')

    # rename foreign keys
    # -------------------

    # rankedgene2genelist
    op.drop_constraint('ranked_gene_2_gene_list_ibfk_1', 'ranked_gene_2_gene_list', type_='foreignkey')
    op.drop_constraint('ranked_gene_2_gene_list_ibfk_2', 'ranked_gene_2_gene_list', type_='foreignkey')
    op.alter_column('ranked_gene_2_gene_list', 'rankedgene_id', new_column_name='ranked_gene_fk', type_=sa.Integer)
    op.alter_column('ranked_gene_2_gene_list', 'genelist_id', new_column_name='gene_list_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'ranked_gene_2_gene_list', 'ranked_gene', ['ranked_gene_fk'], ['id'])
    op.create_foreign_key(None, 'ranked_gene_2_gene_list', 'gene_list', ['gene_list_fk'], ['id'])

    # metadata
    op.drop_constraint('exp_metadata_ibfk_2', 'exp_metadata', type_='foreignkey')
    op.alter_column('exp_metadata', 'extraction_fk', new_column_name='gene_signature_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'exp_metadata', 'gene_signature', ['gene_signature_fk'], ['id'])

    # genelist
    op.drop_constraint('gene_list_ibfk_1', 'gene_list', type_='foreignkey')
    op.alter_column('gene_list', 'extraction_id', new_column_name='gene_signature_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'gene_list', 'gene_signature', ['gene_signature_fk'], ['id'])

    # rankedgene
    op.drop_constraint('ranked_gene_ibfk_1', 'ranked_gene', type_='foreignkey')
    op.alter_column('ranked_gene', 'gene_id', new_column_name='gene_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'ranked_gene', 'gene', ['gene_fk'], ['id'])

    # softfile
    op.drop_constraint('soft_file_ibfk_1', 'soft_file', type_='foreignkey')
    op.alter_column('soft_file', 'extraction_fk', new_column_name='gene_signature_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'soft_file', 'gene_signature', ['gene_signature_fk'], ['id'])

    # tagstoextractions
    op.drop_constraint('tags_to_extractions_ibfk_1', 'tags_to_extractions', type_='foreignkey')
    op.alter_column('tags_to_extractions', 'extraction_fk', new_column_name='gene_signature_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'tags_to_extractions', 'gene_signature', ['gene_signature_fk'], ['id'])
