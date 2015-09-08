"""List of gene symbols with metadata about how the list was created.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
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
    required_metadata = db.relationship('RequiredMetadata', backref=db.backref('gene_lists', order_by=id))
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))
    ranked_genes = db.relationship('RankedGene', secondary=ranked_gene_2_gene_list, backref=db.backref('gene_lists', order_by=id))
    target_app_links = db.relationship("TargetAppLink", backref=db.backref('gene_list', order_by=id))
    text_file = db.Column(db.String(200))

    def __init__(self, ranked_genes, direction, required_metadata, target_app_links):
        """Constructs a gene list.
        """
        self.ranked_genes = ranked_genes
        self.direction = direction,
        self.required_metadata = required_metadata
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
        return {
            'direction': self.direction,
            'ranked_genes': [rg.serialize for rg in self.ranked_genes],
            'target_apps': {
                'enrichr': self.enrichr_link,
                'l1000cds2': self.l1000cds2_link,
                'paea': self.paea_link,
            },
            'text_file': self.text_file
        }