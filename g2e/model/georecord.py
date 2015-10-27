"""Unique gene symbol in a table of canonical symbols.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class GeoRecord(db.Model):

    __tablename__ = 'geo_record'
    id = db.Column(db.Integer, primary_key=True)
    accession = db.Column(db.String(255))
    title = db.Column(db.String(255))
    record_type = db.Column(db.String(32), nullable=False)
    gene_signatures = db.relationship('SoftFile', backref=db.backref('geo_record', order_by=id))
    __mapper_args__ = {'polymorphic_on': record_type}

    def __init__(self, **kwargs):
        self.accession = kwargs['accession']
        self.title = kwargs['title']
        self.record_type = kwargs['record_type']

    def __repr__(self):
        return '<GeoRecord %r>' % self.id
