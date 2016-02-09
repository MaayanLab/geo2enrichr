"""Transforms user input to GeneSignature instance.
"""

from g2e.db.utils import get_or_create
from g2e.endpoints.requestutils import get_param_as_list
from substrate import Tag

from substrate import GeneSignature, OptionalMetadata, Resource, RequiredMetadata
from g2e.signaturefactory import genelistutils, softfileutils
from g2e import db


def from_geo(args):
    """Creates gene signature from GEO data.
    """
    soft_file = softfileutils.maker.from_geo(args)
    return _create_gene_signature(soft_file, args)


def from_file(file_obj, args):
    """Creates an extraction from a custom, uploaded SOFT file.
    """
    soft_file = softfileutils.maker.from_file(file_obj, args)
    return _create_gene_signature(soft_file, args)


def from_gene_list(ranked_genes):
    """Creates gene signature from a pre-existing gene list, not expression
    data.
    """
    return GeneSignature(
        # soft_file,
        # gene_lists,
        # required_metadata,
        # optional_metadata,
        # tags,
        # db.get_or_create(Resource, code='geo')
    )


def _create_gene_signature(soft_file, args):
    """Creates a new extraction, as opposed to an extraction from the
    database.
    """
    required_metadata = _get_required_metadata_from_args(args)
    optional_metadata = _get_optional_metadata_from_args(args)
    tags = _get_tags_from_args(args)

    gene_lists = genelistutils.from_soft_file(
        soft_file,
        required_metadata,
        optional_metadata, tags
    )
    return GeneSignature(
        soft_file,
        gene_lists,
        required_metadata,
        optional_metadata,
        tags,
        db.get_or_create(Resource, code='geo')
    )

def _get_optional_metadata_from_args(args):
    """Helper method for constructing known optional metadata.
    """
    optional_metadata = []
    for key in ['gene', 'cell', 'perturbation', 'disease']:
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


def _get_required_metadata_from_args(args):
    """Constructs a required metadata instance from HTTP request
    arguments.
    """
    diff_exp_method = args['diffexp_method'] if 'diffexp_method' in args else 'chdir'

    # This if-else-iness smells, but I'm not sure what else to do right
    # now. There has to be a better way to handle user input, right?
    if diff_exp_method == 'chdir':
        cutoff = args['cutoff'] if 'cutoff' in args else 500
        if cutoff == 'none' or cutoff == 'None':
            cutoff = None
        else:
            cutoff = int(cutoff)
        ttest_correction_method = None
        threshold = None
    else:
        cutoff = None
        ttest_correction_method = args['correction_method'] if 'correction_method' in args else 'BH'
        if ttest_correction_method == 'none' or ttest_correction_method == 'None':
            ttest_correction_method = None
            threshold = None
        else:
            threshold = args['threshold'] if 'threshold' in args else 0.01
            if threshold == 'none' or threshold == 'None':
                threshold = None
            else:
                threshold = float(threshold)

    return RequiredMetadata(cutoff, threshold, diff_exp_method, ttest_correction_method)


def _get_tags_from_args(args):
    """Returns list of Tag instances.
    """
    tag_names = get_param_as_list(args, 'tags')
    tags = []
    for name in tag_names:
        # If the name is not an empty string or just whitespace.
        if bool(name.strip()):
            tags.append(get_or_create(Tag, name=name))
    return tags
