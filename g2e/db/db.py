"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.
"""

from substrate import GeneSignature, GeoDataset, OptionalMetadata, SoftFile

from g2e.db.utils import session_scope


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


def delete_metadata(extraction_id, metadata_name):
    """Deletes metadata based on extraction ID.
    """
    with session_scope() as session:
        opt = session\
            .query(OptionalMetadata)\
            .join(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .filter(OptionalMetadata.name == metadata_name)\
            .one()

        # No idea why I cannot just chain a delete() call a la
        # delete_gene_signature().
        session.delete(opt)


def edit_metadata(extraction_id, metadata_name):
    """Edits metadata based on extraction ID.
    """
    with session_scope() as session:
        opt = session\
            .query(OptionalMetadata)\
            .join(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .filter(OptionalMetadata.name == metadata_name)\
            .one()

        import pdb; pdb.set_trace()
        session.merge(opt)



def get_geo_dataset(accession):
    """Returns a GEO dataset based on accession number.
    """
    with session_scope() as session:
        instance = session.query(GeoDataset)\
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

