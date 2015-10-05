"""Represents a SoftFile, either from GEO or a user upload, with a link to
the cleaned file and associated metadata.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

import time

from g2e import db
import g2e.core.softfile.softparser as softparser
import g2e.core.softfile.softcleaner as softcleaner
import g2e.core.softfile.softfilemanager as softfilemanager
from g2e.model.softfilesample import SoftFileSample
from g2e.util.requestutil import get_param_as_list
from g2e.dataaccess.util import get_or_create


class SoftFile(db.Model):
    """Metadata for the processed SOFT file.
    """
    __tablename__ = 'soft_file'
    id = db.Column(db.Integer, primary_key=True)
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))
    samples = db.relationship('SoftFileSample', backref='soft_files')
    name = db.Column(db.String(200))
    platform = db.Column(db.String(200))
    is_geo = db.Column(db.Boolean)
    normalize = db.Column(db.Boolean)
    text_file = db.Column(db.String(255))
    actual_text_file = db.Column(db.LargeBinary)

    def __init__(self, name, samples, genes, a_vals, b_vals, platform, text_file, actual_text_file=None, is_geo=False, stats=None, normalize=None):
        """Constructs a SoftFile instance.
        """
        # This should only be called via the class methods.
        self.name = name
        self.samples = samples
        self.genes = genes
        self.is_geo = is_geo
        self.platform = platform
        self.stats = stats
        self.normalize = normalize
        self.text_file = text_file
        self.actual_text_file = actual_text_file

        # These are *not* persisted to the database. Used by diffexp module.
        self.a_vals = a_vals
        self.b_vals = b_vals

    def __repr__(self):
        return '<SoftFile %r>' % self.id

    @classmethod
    def from_geo(cls, args):
        """Constructs a SoftFile
        """
        name = args['dataset']
        if not softfilemanager.file_exists(name):
            softfilemanager.download(name)

        platform = args['platform']
        is_geo = True
        a_cols = get_param_as_list(args, 'A_cols')
        b_cols = get_param_as_list(args, 'B_cols')

        # Use get_or_create to track GSMs. We don't do this for custom files.
        samples = [get_or_create(SoftFileSample, name=sample, is_control=True) for sample in a_cols]\
            + [get_or_create(SoftFileSample, name=sample, is_control=False) for sample in b_cols]

        genes, a_vals, b_vals, selections, stats = softparser.parse(name, is_geo, platform, samples)
        normalize = True if ('normalize' not in args or args['normalize'] == 'True') else False
        genes, a_vals, b_vals = softcleaner.clean(genes, a_vals, b_vals, normalize)

        text_file = softfilemanager.write(name, platform, normalize, genes, a_vals, b_vals, samples, selections, stats)

        return cls(
            name, samples, genes,
            a_vals, b_vals, platform,
            text_file,
            is_geo=is_geo, stats=stats, normalize=normalize
        )

    @classmethod
    def from_file(cls, file_obj, args):
        """Constructs a SoftFile from a user uploaded file.
        """
        if 'name' in args and args['name'] != '':
            name = args['name']
        else:
            name = str(time.time())[:10]
        text_file = softfilemanager.save(name, file_obj)
        genes, a_vals, b_vals, samples = softparser.parse(name, is_geo=False)
        samples = [SoftFileSample(x, True) for x in samples if x == '0']\
            + [SoftFileSample(x, False) for x in samples if x == '1']
        platform = args['platform'] if 'platform' in args else None

        return cls(name, samples, genes, a_vals, b_vals, platform, text_file)

    @property
    def serialize(self):
       """Return serialized object.
       """
       return {
           'name': self.name,
           'normalize': self.normalize,
           'is_geo': self.is_geo,
           'platform': self.platform,
           'text_file': self.text_file
       }