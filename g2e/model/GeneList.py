"""List of gene symbols with metadata about how the list was created.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


rankedgenes_2_genelists = db.Table('rankedgene2genelist', db.metadata,
    db.Column('rankedgene_id', db.Integer, db.ForeignKey('rankedgenes.id')),
    db.Column('genelist_id', db.Integer, db.ForeignKey('genelists.id'))
)


class GeneList(db.Model):
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