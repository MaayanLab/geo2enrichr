"""A supported downstream target application.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class TargetAppLink(db.Model):

    __tablename__ = 'target_app_link'
    id = db.Column(db.Integer, primary_key=True)
    target_app_fk = db.Column(db.Integer, db.ForeignKey('target_app.id'))
    gene_list_fk = db.Column(db.Integer, db.ForeignKey('gene_list.id'))
    link = db.Column(db.Text)

    def __init__(self, target_app, link):
        self.target_app = target_app
        self.link = link

    def __repr__(self):
        return '<TargetAppLink %r>' % self.id