"""Breaking up metadata into required and optional

Revision ID: 4d5f9ba76c5e
Revises: 48957fdfe8d5
Create Date: 2015-08-25 10:35:44.973776

"""

# revision identifiers, used by Alembic.
revision = '4d5f9ba76c5e'
down_revision = '48957fdfe8d5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from substrate import OptionalMetadata, RequiredMetadata, SoftFile


def upgrade():

    # rename tables & columns
    # =======================
    op.rename_table('exp_metadata', 'required_metadata')
    op.rename_table('metadata_tag', 'tag')
    op.rename_table('tags_to_extractions', 'gene_signatures_to_tags')

    # rename columns
    # ==============
    op.drop_constraint('gene_signatures_to_tags_ibfk_2', 'gene_signatures_to_tags', type_='foreignkey')
    op.alter_column('gene_signatures_to_tags', 'metadata_tag_fk', new_column_name='tag_fk', type_=sa.Integer)
    op.create_foreign_key(None, 'gene_signatures_to_tags', 'tag', ['tag_fk'], ['id'])

    # create tables
    # =============
    op.create_table(
        'optional_metadata',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('value', sa.String(255)),
        sa.Column('gene_signature_fk', sa.Integer)
    )
    op.create_foreign_key(None, 'optional_metadata', 'gene_signature', ['gene_signature_fk'], ['id'])

    # Move data
    # =========
    conn = op.get_bind()

    # Move data from required_metadata table to optional_metadata table
    # -----------------------------------------------------------------

    # Move data columns by column
    move_metadata(conn, 'organism')
    move_metadata(conn, 'cell')
    move_metadata(conn, 'gene')
    move_metadata(conn, 'perturbation')
    move_metadata(conn, 'disease')

    # Drop unnecessary columns
    op.drop_column('required_metadata', 'organism')
    op.drop_column('required_metadata', 'cell')
    op.drop_column('required_metadata', 'gene')
    op.drop_column('required_metadata', 'perturbation')
    op.drop_column('required_metadata', 'disease')

    # Move data from diff_exp_method and ttest_correction_method
    # ----------------------------------------------------------

    # Drop constraints so we can modify columns
    op.drop_constraint('required_metadata_ibfk_1', 'required_metadata', type_='foreignkey')
    op.drop_constraint('required_metadata_ibfk_3', 'required_metadata', type_='foreignkey')

    # Rename columns before moving data.
    op.alter_column('required_metadata', 'diff_exp_method_fk', new_column_name='diff_exp_method', type_=sa.String(255))
    op.alter_column('required_metadata', 'ttest_correction_method_fk', new_column_name='ttest_correction_method', type_=sa.String(255))

    # Move methods from their own tables to required_metadata.
    move_method(conn, 'diff_exp_method')
    move_method(conn, 'ttest_correction_method')

    # Drop deprecated tables
    op.drop_table('diff_exp_method')
    op.drop_table('ttest_correction_method')


    # Perform some basic cleanup
    # ==========================

    # This isn't part of the migration per se, but we're performing clean up.
    # These belong (and already exist) on SoftFile.
    op.drop_column('required_metadata', 'normalize')
    op.drop_column('required_metadata', 'platform')

    rebuild_normalize_column(conn)


def move_metadata(conn, name):
    sql = 'SELECT gene_signature_fk, %s FROM required_metadata' % name
    res = conn.execute(sql)
    results = res.fetchall()
    opt_metadata = []
    for r in results:
        if r[1] is not None and r[1] != '':
            opt_metadata.append({ 'gene_signature_fk': r[0], 'name': name, 'value': r[1] })
    op.bulk_insert(OptionalMetadata.__table__, opt_metadata)


def move_method(conn, method):
    sql = 'SELECT %s.name, required_metadata.gene_signature_fk FROM %s '\
          'JOIN required_metadata ON required_metadata.%s = %s.id' % (method, method, method, method)

    tbl = RequiredMetadata.__table__
    res = conn.execute(sql)
    results = res.fetchall()

    for r in results:
        # We cannot assign to r[0]--"TypeError: 'RowProxy' object does not support item assignment"
        if r[0] == 'NA':
            v = None
        else:
            v = r[0]
        stmt = tbl.update(tbl.c.gene_signature_fk == r[1]).values({ method: v })
        conn.execute(stmt)


def rebuild_normalize_column(conn):
    sql = 'SELECT id, normalize FROM soft_file'
    res = conn.execute(sql)
    results = res.fetchall()
    sf_to_normalize = []

    tbl = SoftFile.__table__

    for r in results:
        if r[1] is None:
            v = False
            stmt = tbl.update(tbl.c.id == r[0]).values({ 'normalize': v })
            conn.execute(stmt)