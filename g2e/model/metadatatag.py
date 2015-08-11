"""Groups the Extraction class's various experimental metadata as user inputs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


tags_to_extractions = db.Table('tags_to_extractions', db.metadata,
    db.Column('extraction_fk', db.Integer, db.ForeignKey('extractions.id')),
    db.Column('metadata_tag_fk', db.Integer, db.ForeignKey('metadata_tag.id'))
)


class MetadataTag(db.Model):

    __tablename__ = 'metadata_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    extractions = db.relationship('Extraction', secondary=tags_to_extractions, backref=db.backref('metadata_tags', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Gene %r>' % self.id