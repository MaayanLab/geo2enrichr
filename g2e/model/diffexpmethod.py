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
    extraction = db.relationship('Extraction', uselist=False, backref='diff_exp_method')