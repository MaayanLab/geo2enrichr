"""Unique gene symbol in a table of canonical symbols.
"""


from g2e import db


class Gene(db.Model):
    __tablename__ = 'gene'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ranked_genes = db.relationship("RankedGene", backref=db.backref('gene', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Gene %r>' % self.id