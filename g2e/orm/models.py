from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, backref

# These are references to common instances of SQLAlchemy utilities.
from orm.commondb import Base, engine


association_table = Table('rankedgene2genelist', Base.metadata,
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


class RankedGene(Base):
	"""Gene symbol with an associated pvalue. This does not have to be unique
	and has a many-to-many relationship with a GeneList.
	"""
	__tablename__ = 'rankedgenes'
	id = Column(Integer, primary_key=True)
	pvalue = Column(Integer)
	name = relationship('Gene', backref=backref('rankedgenes', order_by=id))

	def __repr__(self):
		return '<RankedGene %r>' % self.id


class GeneList(Base):
	"""List of gene symbols with metadata about how the list was created.
	"""
	__tablename__ = 'genelists'
	id = Column(Integer, primary_key=True)
	enrichr_link = Column(Text)
	cutoff = Column(Integer)
	diff_exp_method = Column(String(50))

	def __repr__(self):
		return '<GeneList %r>' % self.id


class SoftFile(Base):
	"""List of gene symbols and expression values.
	"""
	__tablename__ = 'softfiles'
	id = Column(Integer, primary_key=True)
	name = Column(Text, unique=True)
	# is_geo == False indicates a custom dataset. 
	is_geo = Column(Boolean)
	# PURPLE_WIRE: Link this table to diseases.

	def __repr__(self):
		return '<SoftFile %r>' % self.id


class Extraction(Base):
	"""Event caused when gene list is extracted from a user uploaded or GEO-
	specified SOFT file.
	"""
	__tablename__ = 'extractions'
	id = Column(Integer, primary_key=True)
	genelist_id = Column(Integer, ForeignKey('genelists.id'))
	# backref allows the GeneList class to reference *all* the extractions in
	# the many-to-one (genelist-to-extraction) relationship.
	genelist = relationship('GeneList', backref=backref('extractions', order_by=id))
	dataset = relationship('SoftFile', backref=backref('softfiles', order_by=id))

	def __repr__(self):
		return '<Extraction %r>' % self.id
