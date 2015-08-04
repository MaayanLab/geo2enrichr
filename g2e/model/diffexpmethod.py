"""Supported differential expression analysis methods.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.app import db


class DiffExpMethod(db.Model):
    __tablename__ = 'diff_exp_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # "noload" means we won't load all the extractions into memory when using
    # this object.
    extractions = db.relationship('Extraction', backref='diff_exp_method', lazy='noload')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<DiffExpMethod %r>' % self.id