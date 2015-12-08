"""List of gene symbols with metadata about how the list was created.
"""


import hashlib

from g2e import db


ranked_gene_2_gene_list = db.Table('ranked_gene_2_gene_list', db.metadata,
    db.Column('ranked_gene_fk', db.Integer, db.ForeignKey('ranked_gene.id')),
    db.Column('gene_list_fk', db.Integer, db.ForeignKey('gene_list.id'))
)


class GeneList(db.Model):

    __tablename__ = 'gene_list'
    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.Integer)
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))
    ranked_genes = db.relationship('RankedGene', secondary=ranked_gene_2_gene_list, backref=db.backref('gene_lists', order_by=id))
    target_app_links = db.relationship("TargetAppLink", backref=db.backref('gene_list', order_by=id))

    def __init__(self, ranked_genes, direction, target_app_links):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.direction = direction
        self.target_app_links = target_app_links

    def __repr__(self):
        return '<GeneList %r>' % self.id

    # PURPLE_WIRE: This should handle duplicate file names, although they are
    # unlikely.
    def _name(self):
        """Hashes the dict of gene,value pairs.
        """
        return hashlib.sha1(str(self.ranked_genes).encode('utf-8')).hexdigest()

    @property
    def serialize(self):
        """Return serialized object.
        """
        target_apps = {}
        for app_link in self.target_app_links:
            key = app_link.target_app.name
            value = app_link.link
            target_apps[key] = value
        return {
            'direction': self.direction,
            'ranked_genes': [rg.serialize for rg in self.ranked_genes],
            'target_apps': target_apps
        }