"""Represents column in a SoftFile, with an indication of whether the column
was used for as a control or an experiment.
"""


from g2e import db


class SoftFileSample(db.Model):
    """List of gene symbols and expression values.
    """
    __tablename__ = 'soft_file_sample'
    id = db.Column(db.Integer, primary_key=True)
    soft_file_fk = db.Column(db.Integer, db.ForeignKey('soft_file.id'))
    name = db.Column(db.String(200))
    is_control = db.Column(db.Boolean)

    def __init__(self, name, is_control):
        """Constructs a SoftFile instance.
        """
        self.name = name
        self.is_control = is_control

    def __repr__(self):
        return '<SoftFileSample %r>' % self.id