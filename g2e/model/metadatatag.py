"""Groups the Extraction class's various experimental metadata as user inputs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


gene_signatures_to_tags = db.Table('gene_signatures_to_tags', db.metadata,
    db.Column('gene_signature_fk', db.Integer, db.ForeignKey('gene_signature.id')),
    db.Column('metadata_tag_fk', db.Integer, db.ForeignKey('metadata_tag.id'))
)


class MetadataTag(db.Model):

    __tablename__ = 'metadata_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gene_signatures = db.relationship('GeneSignature', secondary=gene_signatures_to_tags, backref=db.backref('metadata_tags', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<MetadataTag %r>' % self.id