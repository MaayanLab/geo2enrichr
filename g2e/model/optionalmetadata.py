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

    def __init__(self, experimental_metadata, value):
        """Constructs a Metadata instance.
        """
        self.experimental_metadata = experimental_metadata
        self.value = value

    def __repr__(self):
        return '<OptionalMetadata %r>' % self.id


# TODO: This function should not exist. The front-end should send over an
# 'optionalMetadata' object that can be iterated over and created with an
# arbitrary number of items and values.
#
# The function should look like:
#
# opt_meta_list = []
# for name, value in args.metadata.items():
#     exp_meta = get_or_create(ExperimentalMetadata, name=name)
#     opt_meta = OptionalMetadata(exp_meta, value)
#     opt_meta_list.append(opt_meta)

def construct_opt_meta_from_args(args):
    """Helper method for constructing known optional metadata.
    """
    organism = args['organism'] if 'organism' in args else None
    cell = args['cell'] if 'cell' in args else None
    perturbation = args['perturbation'] if 'perturbation' in args else None
    gene = args['gene'] if 'gene' in args else None
    disease = args['disease'] if 'disease' in args else None

    opt_meta_list = []
    if organism:
        opt_meta = OptionalMetadata('organism', organism)
        opt_meta_list.append(opt_meta)

    if cell:
        opt_meta = OptionalMetadata('cell', cell)
        opt_meta_list.append(opt_meta)

    if perturbation:
        opt_meta = OptionalMetadata('perturbation', perturbation)
        opt_meta_list.append(opt_meta)

    if gene:
        opt_meta = OptionalMetadata('gene', gene)
        opt_meta_list.append(opt_meta)

    if disease:
        opt_meta = OptionalMetadata('organism', disease)
        opt_meta_list.append(opt_meta)

    return opt_meta_list