"""ORM models of all primary data structures and their relationships.

__authors__ = "Gregory Gundersen, Michael McDermott"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, BLOB, Boolean, Float, Integer, String, Text
from sqlalchemy.orm import relationship, backref

# These are references to common instances of SQLAlchemy utilities.
from g2e.orm.commondb import Base, engine


rankedgenes_2_genelists = Table('rankedgene2genelist', Base.metadata,
    Column('rankedgene_id', Integer, ForeignKey('rankedgenes.id')),
    Column('genelist_id', Integer, ForeignKey('genelists.id'))
)


class Gene(Base):
    """Unique gene symbol in a table of canonical symbols.
    """
    __tablename__ = 'genes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Gene %r>' % self.id


class GeneList(Base):
    """List of gene symbols with metadata about how the list was created.
    """
    __tablename__ = 'genelists'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    direction = Column(Integer)
    extraction_id = Column(Integer, ForeignKey('extractions.id'))
    ranked_genes = relationship('RankedGene', secondary=rankedgenes_2_genelists, backref=backref('genelists', order_by=id))
    text_file = Column(String(200))
    enrichr_link = Column(Text)
    l1000cds2_link = Column(Text)
    paea_link = Column(Text)

    def __repr__(self):
        return '<GeneList %r>' % self.id


class RankedGene(Base):
    """Gene symbol with an associated rank. This does not have to be unique
    and has a many-to-many relationship with a GeneList.
    """
    __tablename__ = 'rankedgenes'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    value_type = Column(String(200))
    gene = relationship('Gene', backref=backref('rankedgenes', order_by=id))
    gene_id = Column(Integer, ForeignKey('genes.id'))

    def __repr__(self):
        return '<RankedGene %r>' % self.id


# PURPLE_WIRE: Link this table to diseases.
# PURPLE_WIRE: GEO SoftFiles should be unique, but it's more important that we
# collect at all.
class SoftFile(Base):
    """List of gene symbols and expression values.
    """
    __tablename__ = 'softfiles'
    id = Column(Integer, primary_key=True)
    extraction_id = Column(Integer, ForeignKey('extractions.id'))
    name = Column(String(200))
    platform = Column(String(200))
    # is_geo == False indicates a custom dataset.
    is_geo = Column(Boolean)
    normalize = Column(Boolean)
    text_file = Column(String(200))

    def __repr__(self):
        return '<SoftFile %r>' % self.id


class Extraction(Base):
    """Event caused when gene list is extracted from a user uploaded or GEO-
    specified SOFT file.
    """
    __tablename__ = 'extractions'
    id = Column(Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = Column(String(10))
    softfile = relationship('SoftFile', uselist=False, backref='extractions')
    genelists = relationship('GeneList', backref=backref('genelists', order_by=id))
    diffexp_method = Column(String(200))
    cutoff = Column(Integer)
    correction_method = Column(String(200))
    threshold = Column(Float)
    organism = Column(String(200)) 
    cell = Column(String(200))
    perturbation = Column(String(200))
    gene = Column(String(200))
    disease = Column(String(200))

    def __repr__(self):
        return '<Extraction %r>' % self.id


# This is what rebuilds the database or adds tables as necessary.
Base.metadata.create_all(engine)
