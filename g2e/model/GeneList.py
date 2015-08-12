"""List of gene symbols with metadata about how the list was created.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib

from g2e import db
import g2e.core.genelist.genelistfilemanager as filemanager


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

    def __init__(self, ranked_genes, direction, metadata, target_apps, name=None, text_file=None):
        """Constructs a gene list.
        """
        self.ranked_genes   = ranked_genes
        self.direction      = direction
        self.name           = name or self._name()
        self.enrichr_link   = target_apps['enrichr']
        self.l1000cds2_link = target_apps['l1000cds2']
        self.paea_link      = target_apps['paea']
        self.text_file      = text_file or filemanager.write(
            self.name,
            self.direction,
            self.ranked_genes,
            metadata
        )

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
            'name': self.name,
            'direction': self.direction,
            'ranked_genes': [rg.serialize for rg in self.ranked_genes],
            'target_apps': {
                'enrichr': self.enrichr_link,
                'l1000cds2': self.l1000cds2_link,
                'paea': self.paea_link,
            },
            'text_file': self.text_file
        }