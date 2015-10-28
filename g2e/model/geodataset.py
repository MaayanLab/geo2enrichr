"""Parent class for GEO record subclasses: GeoDataset (GDS), GeoProfile (GSE),
and GeoPlatform (GPL).

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db
from g2e.model.dataset import Dataset


class GeoDataset(Dataset):

    accession = db.Column(db.String(255), unique=True)
    platform = db.Column(db.String(32))
    __mapper_args__ = {'polymorphic_identity': 'geo'}

    def __init__(self, **kwargs):
        super(GeoDataset, self).__init__(**kwargs)
        self.accession = kwargs['accession']
        self.platform = 'GPL' + kwargs['platform']
        self.is_gds = ('GDS' in self.accession)

    def __repr__(self):
        return '<GeoDataset %r>' % self.id
