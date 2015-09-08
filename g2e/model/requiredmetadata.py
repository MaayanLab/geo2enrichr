"""Required metadata for a gene signature extraction.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class RequiredMetadata(db.Model):

    __tablename__ = 'required_metadata'
    id = db.Column(db.Integer, primary_key=True)
    diff_exp_method = db.Column(db.String(255))
    ttest_correction_method = db.Column(db.String(255))
    cutoff = db.Column(db.Integer)
    threshold = db.Column(db.Float)
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))

    def __init__(self, cutoff, threshold, diff_exp_method, ttest_correction_method):
        """Constructs a Metadata instance.
        """
        self.cutoff = cutoff
        self.threshold = threshold
        self.diff_exp_method = diff_exp_method
        self.ttest_correction_method = ttest_correction_method

    def __repr__(self):
        return '<RequiredMetadata %r>' % self.id

    @classmethod
    def from_args(cls, args):
        """Constructs a required metadata instance from HTTP request
        arguments.
        """
        diff_exp_method = args['diffexp_method'] if 'diffexp_method' in args else 'chdir'
        
        # This if-else-iness smells, but I'm not sure what else to do right
        # now. There has to be a better way to handle user input, right?
        if diff_exp_method == 'chdir':
            cutoff = args['cutoff'] if 'cutoff' in args else 500
            if cutoff == 'none' or cutoff == 'None':
                cutoff = None
            else:
                cutoff = int(cutoff)
            ttest_correction_method = None
            threshold = None
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

        return cls(cutoff, threshold, diff_exp_method, ttest_correction_method)

    def __str__(self):
        """Stringifies the metadata instance.
        """
        # This is used primarily for sending a description to third-party
        # target applications.
        result = []
        for key,val in self.__dict__.items():
            # Ignore SQLAlchemy relationships, e.g. gene_signature_fk.
            if key == '_sa_instance_state':
                continue
            if val:
                result.append(str(val))
        return '-'.join(result)

    def to_L1000CDS2_data_format(self):
        """Formats the metadata for L1000CDS2 target application.
        """
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
            'diff_exp_method': self.diff_exp_method,
            'ttest_correction_method': self.ttest_correction_method
        }