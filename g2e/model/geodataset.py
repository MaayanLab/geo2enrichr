"""Unique gene symbol in a table of canonical symbols.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db
from g2e.model.georecord import GeoRecord


class GeoDataset(GeoRecord):

    summary = db.Column(db.Text)
    __mapper_args__ = {'polymorphic_identity': 'dataset'}

    def __init__(self, **kwargs):
        super(GeoRecord, self).__init__(**kwargs)
        self.summary = kwargs['summary']

    def __repr__(self):
        return '<GeoDataset %r>' % self.id
