"""Event caused when gene list is extracted from a user uploaded or GEO-
specified SOFT file.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


class Extraction(db.Model):
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