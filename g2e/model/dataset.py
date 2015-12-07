"""Parent class for GEO record subclasses: GeoDataset (GDS), GeoProfile (GSE),
and GeoPlatform (GPL).
"""


from g2e import db


class Dataset(db.Model):

    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    record_type = db.Column(db.String(32), nullable=False)
    summary = db.Column(db.Text)
    organism = db.Column(db.String(255))

    __mapper_args__ = {'polymorphic_on': record_type}

    # Back references.
    soft_files = db.relationship('SoftFile', backref=db.backref('dataset', order_by=id))

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        if 'summary' in kwargs:
            self.summary = kwargs['summary']
        if 'organism' in kwargs:
            self.organism = kwargs['organism']

    def __repr__(self):
        return '<Dataset %r>' % self.id
