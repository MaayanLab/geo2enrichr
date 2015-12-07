"""Represents a SoftFile, either from GEO or a user upload, with a link to
the cleaned file and associated metadata.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

import time

from g2e import db
import g2e.core.softfile.softfileparser as softparser
import g2e.core.softfile.softcleaner as softcleaner
import g2e.core.softfile.softfilemanager as softfilemanager
from g2e.model.softfilesample import SoftFileSample
from g2e.util.requestutil import get_param_as_list
from g2e.dataaccess.util import get_or_create
from g2e.model.geodataset import GeoDataset
from g2e.model.customdataset import CustomDataset
from g2e.dataaccess import datasetdal


class SoftFile(db.Model):
    """Metadata for the processed SOFT file.
    """
    __tablename__ = 'soft_file'
    id = db.Column(db.Integer, primary_key=True)

    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'), nullable=False)
    dataset_fk = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    samples = db.relationship('SoftFileSample', backref='soft_files')

    normalize = db.Column(db.Boolean)
    text_file = db.Column(db.String(255))

    # TODO: Drop after transfering data!
    is_geo = db.Column(db.Boolean)
    name = db.Column(db.String(200))

    def __init__(self, samples, dataset, text_file, genes, a_vals, b_vals, normalize=False, stats=None):
        """Constructs a SoftFile instance.
        """
        self.samples = samples
        self.dataset = dataset
        self.text_file = text_file
        self.normalize = normalize

        # These are *not* persisted to the database. Used by diffexp module.
        self.genes = genes
        self.a_vals = a_vals
        self.b_vals = b_vals
        self.stats = stats

    def __repr__(self):
        return '<SoftFile %r>' % self.id

    @classmethod
    def from_geo(cls, args):
        """Constructs a SoftFile
        """
        accession = args['dataset']

        if not softfilemanager.file_exists(accession):
            softfilemanager.download(accession)

        dataset = datasetdal.get(accession)
        if dataset == None:
            platform = args['platform']
            if platform.index('GPL') == 0:
                platform = platform[3:]
            organism = args['organism'] if 'organism' in args else 'TODO'
            title = args['title']       if 'title'    in args else 'TODO'
            summary = args['summary']   if 'summary'  in args else 'TODO'
            dataset = GeoDataset(
                accession=accession,
                platform=platform,
                organism=organism,
                title=title,
                summary=summary
            )
        else:
            print 'Dataset %s already exists!' % accession

        a_cols = get_param_as_list(args, 'A_cols')
        b_cols = get_param_as_list(args, 'B_cols')

        # Use get_or_create to track GSMs. We don't do this for custom files.
        control      = [get_or_create(SoftFileSample, name=sample, is_control=True)  for sample in a_cols]
        experimental = [get_or_create(SoftFileSample, name=sample, is_control=False) for sample in b_cols]
        samples = control + experimental

        genes, a_vals, b_vals, selections, stats = softparser.parse(accession, True, dataset.platform, samples)
        normalize = True if ('normalize' not in args or args['normalize'] == 'True') else False
        genes, a_vals, b_vals = softcleaner.clean(genes, a_vals, b_vals, normalize)

        text_file = softfilemanager.write(accession, dataset.platform, normalize, genes, a_vals, b_vals, samples, selections, stats)

        return cls(
            samples, dataset, text_file,
            genes, a_vals, b_vals,
            stats=stats, normalize=normalize
        )

    @classmethod
    def from_file(cls, file_obj, args):
        """Constructs a SoftFile from a user uploaded file.
        """
        # We support name and title for historical reasons, i.e. Firefox
        # support since we won't be releasing new versions of the add on.
        if 'name' in args and args['name'] != '':
            title = args['name']
        elif 'title' in args and args['title'] != '':
            title = args['title']
        else:
            title = str(time.time())[:10]

        text_file = softfilemanager.save(title, file_obj)
        genes, a_vals, b_vals, samples = softparser.parse(title, is_geo=False)

        control =      [SoftFileSample(x[0], True)  for x in samples if x[1] == '0']
        experimental = [SoftFileSample(x[0], False) for x in samples if x[1] == '1']
        samples = control + experimental

        organism = args['organism'] if 'organism' in args else None

        dataset = CustomDataset(
            title=title,
            organism=organism
        )
        return cls(samples, dataset, text_file, genes, a_vals, b_vals)

    @property
    def serialize(self):
        """Return serialized object.
        """
        if hasattr(self.dataset, 'platform'):
            platform = self.dataset.platform
        else:
            platform = None

        if hasattr(self.dataset, 'accession'):
            accession = self.dataset.accession
        else:
            accession = None

        if self.samples:
            selected_samples = [{'name':x.name, 'is_control':x.is_control} for x in self.samples]
        else:
            selected_samples = 'na'

        return {
            'title': self.dataset.title,
            'accession': accession,
            'normalize': self.normalize,
            'is_geo': self.dataset.record_type == 'geo',
            'platform': platform,
            'organism': self.dataset.organism,
            'text_file': self.text_file,
            'selected_samples': selected_samples
        }

    def get_raw_data(self):
        """Returns the raw data a two-dimensional array.
        """
        results = []
        f = file('g2e/' + self.text_file)
        for i,line in enumerate(f):
            if i < 8:
                continue
            line = line.strip()
            results.append(line.split('\t'))
        return results
