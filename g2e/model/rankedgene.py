"""Gene symbol with an associated rank. This does not have to be unique
and has a many-to-many db.relationship with a GeneList.
"""


from g2e import db


class RankedGene(db.Model):

    __tablename__ = 'ranked_gene'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    gene_fk = db.Column(db.Integer, db.ForeignKey('gene.id'))

    def __init__(self, gene, value):
        self.gene = gene
        self.value = value

    def __repr__(self):
        return '<RankedGene %r>' % self.id

    @property
    def serialize(self):
       """Return serialized object.
       """
       return [self.gene.name, self.value]