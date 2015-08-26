"""Groups the Extraction class's various experimental metadata as user inputs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db
from g2e.dataaccess.util import get_or_create
from g2e.util.requestutil import get_param_as_list

gene_signatures_to_tags = db.Table('gene_signatures_to_tags', db.metadata,
    db.Column('gene_signature_fk', db.Integer, db.ForeignKey('gene_signature.id')),
    db.Column('tag_fk', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):

    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gene_signatures = db.relationship('GeneSignature', secondary=gene_signatures_to_tags, backref=db.backref('tags', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.id

    @classmethod
    def from_args(cls, args):
        tag_names = get_param_as_list(args, 'tags')
        tags = []
        for name in tag_names:
            # If the name is not an empty string or just whitespace.
            if bool(name.strip()):
                tags.append(get_or_create(Tag, name=name))
        return tags