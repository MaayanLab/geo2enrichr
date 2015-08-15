"""Supported t-test correction methods.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class TtestCorrectionMethod(db.Model):

    __tablename__ = 'ttest_correction_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    exp_metadata = db.relationship('ExpMetadata', backref='ttest_correction_method')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<TtestCorrectionMethod %r>' % self.id