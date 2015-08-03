"""ORM models of all primary data structures and their db.relationships.

__authors__ = "Gregory Gundersen, Michael McDermott"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


rankedgenes_2_genelists = db.Table('rankedgene2genelist', db.metadata,
    db.Column('rankedgene_id', db.Integer, db.ForeignKey('rankedgenes.id')),
    db.Column('genelist_id', db.Integer, db.ForeignKey('genelists.id'))
)


class Gene(db.Model):
    """Unique gene symbol in a table of canonical symbols.
    """
    __tablename__ = 'genes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Gene %r>' % self.id


class GeneList(db.Model):
    """List of gene symbols with metadata about how the list was created.
    """
    __tablename__ = 'genelists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    direction = db.Column(db.Integer)
    extraction_id = db.Column(db.Integer, db.ForeignKey('extractions.id'))
    ranked_genes = db.relationship('RankedGene', secondary=rankedgenes_2_genelists, backref=db.backref('genelists', order_by=id))
    text_file = db.Column(db.String(200))
    enrichr_link = db.Column(db.Text)
    l1000cds2_link = db.Column(db.Text)
    paea_link = db.Column(db.Text)

    def __repr__(self):
        return '<GeneList %r>' % self.id


class RankedGene(db.Model):
    """Gene symbol with an associated rank. This does not have to be unique
    and has a many-to-many db.relationship with a GeneList.
    """
    __tablename__ = 'rankedgenes'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    value_type = db.Column(db.String(200))
    gene = db.relationship('Gene', backref=db.backref('rankedgenes', order_by=id))
    gene_id = db.Column(db.Integer, db.ForeignKey('genes.id'))

    def __repr__(self):
        return '<RankedGene %r>' % self.id


class Extraction(db.Model):
    """Event caused when gene list is extracted from a user uploaded or GEO-
    specified SOFT file.
    """
    __tablename__ = 'extractions'
    id = db.Column(db.Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = db.Column(db.String(10))
    softfile = db.relationship('SoftFile', uselist=False, backref='extractions')
    genelists = db.relationship('GeneList', backref=db.backref('genelists', order_by=id))

    diff_exp_method_fk = db.Column(db.Integer, db.ForeignKey('diff_exp_method.id'))
    ttest_correction_method_fk = db.Column(db.Integer, db.ForeignKey('ttest_correction_method.id'))

    cutoff = db.Column(db.Integer)
    threshold = db.Column(db.Float)
    organism = db.Column(db.String(255))
    cell = db.Column(db.String(255))
    perturbation = db.Column(db.String(255))
    gene = db.Column(db.String(255))
    disease = db.Column(db.String(255))

    def __repr__(self):
        return '<Extraction %r>' % self.id


class DiffExpMethod(db.Model):
    """Supported differential expression analysis methods.
    """
    __tablename__ = 'diff_exp_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    extraction = db.relationship('Extraction', uselist=False, backref='diff_exp_method')


class TtestCorrectionMethod(db.Model):
    """Supported t-test correction methods.
    """
    __tablename__ = 'ttest_correction_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    extraction = db.relationship('Extraction', uselist=False, backref='ttest_correction_method')
