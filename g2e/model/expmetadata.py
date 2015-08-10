"""Groups the Extraction class's various experimental metadata as user inputs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db
from g2e.dao.util import get_or_create
from g2e.model.diffexpmethod import DiffExpMethod
from g2e.model.ttestcorrectionmethod import TtestCorrectionMethod


class ExpMetadata(db.Model):

    __tablename__ = 'exp_metadata'
    id = db.Column(db.Integer, primary_key=True)
    extraction_fk = db.Column(db.Integer, db.ForeignKey('extractions.id'))
    diff_exp_method_fk = db.Column(db.Integer, db.ForeignKey('diff_exp_method.id'))
    ttest_correction_method_fk = db.Column(db.Integer, db.ForeignKey('ttest_correction_method.id'))

    cutoff = db.Column(db.Integer)
    threshold = db.Column(db.Float)
    organism = db.Column(db.String(255))
    cell = db.Column(db.String(255))
    perturbation = db.Column(db.String(255))
    gene = db.Column(db.String(255))
    disease = db.Column(db.String(255))
    platform = db.Column(db.String(255))
    normalize = db.Column(db.Boolean)

    def __init__(self, cutoff, threshold, organism, cell, perturbation, gene, disease, diff_exp_method=None, ttest_correction_method=None, platform=None, normalize=None):
        """Constructs a Metadata instance.
        """
        self.cutoff = cutoff
        self.threshold = threshold
        self.organism = organism
        self.cell = cell
        self.perturbation = perturbation
        self.gene = gene
        self.disease = disease
        self.platform = platform
        self.normalize = normalize

        if diff_exp_method:
            self.diff_exp_method = get_or_create(DiffExpMethod, name=diff_exp_method)
        if ttest_correction_method:
            self.ttest_correction_method = get_or_create(TtestCorrectionMethod, name=ttest_correction_method)

    @classmethod
    def from_args(cls, args):
        """Constructs a metadata instance from arguments as opposed to the
        database.
        """
        diff_exp_method = args['diffexp_method'] if 'diffexp_method' in args else 'chdir'
        
        # This if-else-iness smells, but I'm not sure what else to do right
        # now. There has to be a better way to handle user input, right?
        if diff_exp_method == 'chdir':
            cutoff = args['cutoff'] if 'cutoff' in args else 500
            ttest_correction_method = 'NA'
            threshold = None
            if cutoff == 'none' or cutoff == 'None':
                cutoff = None
            else:
                cutoff = int(cutoff)
        else:
            cutoff = None
            ttest_correction_method = args['correction_method'] if 'correction_method' in args else 'BH'
            if ttest_correction_method == 'none' or ttest_correction_method == 'None':
                ttest_correction_method = None
                threshold = None
            else:
                threshold = args['threshold'] if 'threshold' in args else 0.01
                if threshold == 'none' or threshold == 'None':
                    threshold = None
                else:
                    threshold = float(threshold)

        print 'ttest_correction_method: ' + str(ttest_correction_method)
        print 'threshold: ' + str(threshold)

        organism = args['organism'] if 'organism' in args else None
        cell = args['cell'] if 'cell' in args else None
        perturbation = args['perturbation'] if 'perturbation' in args else None
        gene = args['gene'] if 'gene' in args else None
        disease = args['disease'] if 'disease' in args else None

        # This metadata is actually in the SoftFile instance as well, but
        # adding it here makes it easier to add to the description passed to
        # the target applications.
        platform = args['platform'] if 'platform' in args else None
        normalize = True if ('normalize' not in args or args['normalize'] == 'True') else False
        return cls(cutoff, threshold, organism, cell, perturbation, gene, disease, diff_exp_method, ttest_correction_method, platform, normalize)

    def __str__(self):
        """Stringifies the metadata instance.
        """
        # This is used primarily for sending a description to third-party
        # target applications.
        result = []
        for key,val in self.__dict__.items():
            if val:
                result.append(str(val))
        return '-'.join(result)

    def to_L1000CDS2_data_format(self):
        result = []
        for key,val in self.serialize.items():
            result.append({
                'key': key,
                'value': val
            })
        return result

    @property
    def serialize(self):
        return {
            'cutoff': self.cutoff,
            'threshold': self.threshold,
            'organism': self.organism,
            'cell': self.cell,
            'perturbation': self.perturbation,
            'gene': self.gene,
            'disease': self.disease,
            'platform': self.platform,
            'normalize': self.normalize,
            'diff_exp_method': self.diff_exp_method.name if self.diff_exp_method else None,
            'ttest_correction_method': self.ttest_correction_method.name  if self.ttest_correction_method else None
        }