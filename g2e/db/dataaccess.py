"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.
"""


import sqlalchemy as sa

from substrate import GeneList
from substrate import GeneSignature
from substrate import SoftFile
from substrate import Tag
from substrate import GeoDataset
from substrate import OptionalMetadata

from g2e.db.utils import session_scope


def fetch_all(klass):
    """Fetches all entities of a specific class.
    """
    with session_scope() as session:
        return session.query(klass).all()


def save_gene_signature(gene_signature):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        session.add(gene_signature)
        session.commit()
        return gene_signature.extraction_id


def fetch_gene_signature(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .first()


def fetch_tag(tag_name):
    """Fetches tags based on name.
    """
    with session_scope() as session:
        return session\
            .query(Tag)\
            .filter(Tag.name == tag_name)\
            .first()


def fetch_metadata(metadata_name):
    """Fetches metadata based on name.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .all()


def fetch_metadata_by_value(metadata_name, metadata_value):
    """Fetches metadata based on name and value.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .filter(OptionalMetadata.value == metadata_value)\
            .all()


def get_dataset(accession):
    with session_scope() as session:
        instance = session.query(GeoDataset)\
            .filter_by(accession=accession)\
            .first()
        return instance


def get_suggestions(query):
    suggestions = []
    suggestions += _get_optional_metadata_suggestions(query) or []
    return suggestions


def _get_optional_metadata_suggestions(query):
    with session_scope() as session:
        query_results = []
        query_results += session\
            .execute('SELECT value FROM optional_metadata '
                     'WHERE MATCH(value) AGAINST(:query IN BOOLEAN MODE)',
                     {'query': query})\
            .fetchall()
        query_results += session\
            .execute('SELECT value FROM optional_metadata '
                     'WHERE value SOUNDS LIKE :query',
                     {'query': query})\
            .fetchall()
        query_results += session\
            .execute('SELECT value FROM optional_metadata '
                     'WHERE value LIKE :query',
                     {'query': query})\
            .fetchall()

        suggestions = [x[0] for x in query_results]
        seen = set()
        for x in suggestions:
            seen.add(x)
        return seen


def get_statistics():
    """Returns hash with DB statistics for about page.
    """
    with session_scope() as session:
        num_gene_signatures = session.query(GeneSignature).count()
        num_gene_lists = session.query(GeneList).count()
        num_tags = session.query(Tag).count()
        platforms = session.query(sa.func.distinct(GeoDataset.platform))

        platform_counts = []
        for tpl in platforms:
            platform = tpl[0]
            count = session.query(GeneSignature, SoftFile, GeoDataset)\
                .filter(SoftFile.dataset_fk == GeoDataset.id)\
                .filter(SoftFile.gene_signature_fk == GeneSignature.id)\
                .filter(GeoDataset.platform == platform)\
                .count()
            platform_counts.append({
                'platform': platform,
                'count': count
            })

        return {
            'num_gene_signatures': num_gene_signatures,
            'num_gene_lists': num_gene_lists,
            'num_tags': num_tags,
            'num_platforms': len(platform_counts),
            'platform_counts': platform_counts
        }