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

from g2e.app import db
from g2e.model.softfile import SoftFile
from g2e.core.metadata.metadata import Metadata
from g2e.model.diffexpmethod import DiffExpMethod
from g2e.model.ttestcorrectionmethod import TtestCorrectionMethod
from g2e.core.genelist.genelistsmaker import genelists_maker
from g2e.dao.util import get_or_create


class Extraction(db.Model):

    __tablename__ = 'extractions'
    id = db.Column(db.Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = db.Column(db.String(10))
    softfile = db.relationship('SoftFile', uselist=False, backref='extractions')
    genelists = db.relationship('GeneList', backref=db.backref('genelists', order_by=id))

    diff_exp_method_fk = db.Column(db.Integer, db.ForeignKey('diff_exp_method.id'))
    ttest_correction_method_fk = db.Column(db.Integer, db.ForeignKey('ttest_correction_method.id'))

    cutoff = db.Column(db.Integer)
    threshold = db.Column(db.Float)
    organism = db.Column(db.String(255))
    cell = db.Column(db.String(255))
    perturbation = db.Column(db.String(255))
    gene = db.Column(db.String(255))
    disease = db.Column(db.String(255))

    def __init__(self, softfile, genelists, exp_metadata):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        # This is *not* the database ID. This is hashed so that users cannot
        # simply guess the ID for other user's data.
        self.extraction_id = hashlib.sha1(str(time.time())).hexdigest()[:10]
        self.softfile  = softfile
        self.genelists = genelists

        # TODO: This is *awful*. We're storing everything on the extraction
        # rather than persisting it via a metadata table.
        self.cutoff = exp_metadata.cutoff
        self.threshold = exp_metadata.threshold
        self.organism = exp_metadata.organism
        self.cell = exp_metadata.cell
        self.gene = exp_metadata.gene
        self.disease = exp_metadata.disease

        if exp_metadata.diffexp_method:
            self.diff_exp_method = get_or_create(DiffExpMethod, name=exp_metadata.diffexp_method)
        if exp_metadata.correction_method:
            self.ttest_correction_method = get_or_create(TtestCorrectionMethod, name=exp_metadata.correction_method)

    def __repr__(self):
        return '<Extraction %r>' % self.id

    @classmethod
    def new(cls, softfile, args):
        """Creates a new extraction, as opposed to an extraction from the
        database.
        """
        exp_metadata = Metadata.from_args(args)
        skip_target_apps = True if 'skip_targets_apps' in args else False
        if skip_target_apps:
            print 'skipping target applications'
        genelists = genelists_maker(softfile, exp_metadata, skip_target_apps)
        return cls(softfile, genelists, exp_metadata)

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
            'metadata': Metadata.from_extraction(self).__dict__,
        }