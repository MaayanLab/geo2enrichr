"""Unique gene symbol in a table of canonical symbols.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class AccessionNumber(db.Model):
    __tablename__ = 'accession_number'
    id = db.Column(db.Integer, primary_key=True)
    gene_signatures = db.relationship('SoftFile', backref=db.backref('accession_number', order_by=id))

    def __init__(self, geo_id):
        self.geo_id = geo_id
        if 'GDS' in self.geo_id:
            self.is_gds = True
        else:
            self.is_gds = False

    def __repr__(self):
        return '<AccessionNumber %r>' % self.id
