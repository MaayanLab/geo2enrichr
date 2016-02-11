"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.
"""

from substrate import GeneSignature, GeoDataset, SoftFile, Tag

from g2e.database.utils import session_scope


def get_gene_signature(extraction_id):
    """Returns gene signature based on extraction ID.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .first()


def save_gene_signature(gene_signature):
    """Saves a gene signature and returns the extraction ID.
    """
    with session_scope() as session:
        session.add(gene_signature)
        session.commit()
        return gene_signature.extraction_id


def delete_gene_signature(extraction_id):
    """Deletes a gene signature by extraction ID.
    """
    with session_scope() as session:
        session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .delete()


def get_tag_by_name(tag_name):
    """Returns tag by name.
    """
    with session_scope() as session:
        return session\
            .query(Tag)\
            .filter_by(name=tag_name)\
            .first()


def delete_object(obj):
    """Deletes object provided.
    """
    with session_scope() as session:
        session.delete(obj)


def update_object(obj):
    """Update object, i.e. saves any edits.
    """
    with session_scope() as session:
        session.merge(obj)


def get_geo_dataset(accession):
    """Returns a GEO dataset based on accession number.
    """
    with session_scope() as session:
        instance = session\
            .query(GeoDataset)\
            .filter_by(accession=accession)\
            .first()
        return instance


def get_num_gene_signatures():
    """Returns the number of gene signatures in the database.
    """
    with session_scope() as session:
        return session.query(GeneSignature).count()


def get_soft_files_by_accession(accession):
    """Returns a list of SOFT files based on a GEO dataset accession ID.
    """
    with session_scope() as session:
        return session\
            .query(SoftFile)\
            .filter(SoftFile.dataset_fk == GeoDataset.id)\
            .filter(GeoDataset.accession == accession)\
            .all()

