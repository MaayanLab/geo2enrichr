"""Event caused when gene list is extracted from a user uploaded or GEO-
specified SOFT file.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""



"""Creates an Extraction, which represents a single instance of a user's
processed data, with links to the SOFT file, gene lists, and metadata.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import time

from g2e import db
from g2e.dataaccess.util import get_or_create
from g2e.model.softfile import SoftFile
from g2e.model.expmetadata import ExpMetadata
from g2e.model.metadatatag import MetadataTag
from g2e.core.genelist.genelistsmaker import genelists_maker


class GeneSignature(db.Model):

    __tablename__ = 'gene_signature'
    id = db.Column(db.Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = db.Column(db.String(10))
    softfile = db.relationship('SoftFile', uselist=False, backref='gene_signatures')
    genelists = db.relationship('GeneList', backref=db.backref('gene_signature', order_by=id))
    exp_metadata = db.relationship('ExpMetadata', uselist=False, backref=db.backref('gene_signature', order_by=id))

    def __init__(self, softfile, genelists, exp_metadata, metadata_tags):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        # This is *not* the database ID. This is hashed so that users cannot
        # simply guess the ID for other user's data.
        self.extraction_id = hashlib.sha1(str(time.time())).hexdigest()[:10]
        self.softfile  = softfile
        self.genelists = genelists
        self.exp_metadata  = exp_metadata
        self.metadata_tags = metadata_tags

    def __repr__(self):
        return '<GeneSignature %r>' % self.id

    @classmethod
    def new(cls, softfile, args):
        """Creates a new extraction, as opposed to an extraction from the
        database.
        """
        exp_metadata = ExpMetadata.from_args(args)
        if 'tags' in args:
            tags = args.get('tags').split(',')
        else:
            tags = []
        metadata_tags = [get_or_create(MetadataTag, name=name) for name in tags]
        genelists = genelists_maker(softfile, exp_metadata)
        return cls(softfile, genelists, exp_metadata, metadata_tags)

    @classmethod
    def from_geo(cls, args):
        """Creates an extraction from GEO data.
        """
        softfile = SoftFile.from_geo(args)
        return cls.new(softfile, args)

    @classmethod
    def from_file(cls, file_obj, args):
        """Creates an extraction from a custom, uploaded SOFT file.
        """
        # PURPLE_WIRE: Users *will* upload bad data and parsing their files
        # *will* throw an error. Catch and handle appropriately.
        softfile = SoftFile.from_file(file_obj, args)
        return cls.new(softfile, args)

    @property
    def serialize(self):
        return {
            'extraction_id': self.extraction_id,
            'softfile': self.softfile.serialize,
            'genelists': [gl.serialize for gl in self.genelists],
            'metadata': self.exp_metadata.serialize,
            'tags': [t.name for t in self.metadata_tags]
        }