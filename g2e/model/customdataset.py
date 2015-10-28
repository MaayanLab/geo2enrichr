"""Custom data source record uploaded by user.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e.model.dataset import Dataset


class CustomDataset(Dataset):

    __mapper_args__ = {'polymorphic_identity': 'custom'}

    def __init__(self, **kwargs):
        super(CustomDataset, self).__init__(**kwargs)

    def __repr__(self):
        return '<CustomDataset %r>' % self.id
