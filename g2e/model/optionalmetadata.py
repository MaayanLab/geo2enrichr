"""Optional metadata for a gene signature extraction.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class OptionalMetadata(db.Model):

    __tablename__ = 'optional_metadata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))

    def __init__(self, name, value):
        """Constructs a Metadata instance.
        """
        self.name = name
        self.value = value

    def __repr__(self):
        return '<OptionalMetadata %r>' % self.id

    @classmethod
    def from_args(cls, args):
        """Helper method for constructing known optional metadata.
        """
        optional_metadata = []
        for key in ['organism', 'cell', 'perturbation', 'disease']:
            if key in args:
                value = args[key]
                optional_metadata.append(OptionalMetadata(key, value))

        # This is a hack, but I don't want to refactor too much right now.
        # An HTML form does not support nesting of fields, but we need to
        # to know which fields are arbitrary metadata. I noticed that they
        # are rendered as the string:
        #
        #     metadata[<field name>]
        #
        # Thus, we iterate, looking for these properties. The alternative to
        # this approach would require POSTing the file and JSON metadata
        # separately. See:
        #
        # http://stackoverflow.com/questions/3938569
        for key in args:
            if 'metadata[' in key:
                # Remove the 'Metadata[]' from around the field name.
                # I know this sucks.
                name = key[9:]
                name = name[:-1]
                optional_metadata.append(OptionalMetadata(name, args[key]))

        return optional_metadata
