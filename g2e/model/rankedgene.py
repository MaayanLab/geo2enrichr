"""Gene symbol with an associated rank. This does not have to be unique
and has a many-to-many db.relationship with a GeneList.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


class RankedGene(db.Model):
    __tablename__ = 'rankedgenes'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    value_type = db.Column(db.String(200))
    gene = db.relationship('Gene', backref=db.backref('rankedgenes', order_by=id))
    gene_id = db.Column(db.Integer, db.ForeignKey('genes.id'))

    def __repr__(self):
        return '<RankedGene %r>' % self.id

