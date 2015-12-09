"""
"""


from substrate import OptionalMetadata


def from_args(args):
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