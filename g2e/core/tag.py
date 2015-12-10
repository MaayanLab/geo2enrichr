"""
"""

from substrate import Tag
from g2e.db.utils import get_or_create
from g2e.utils.requestutil import get_param_as_list


def from_args(args):
    tag_names = get_param_as_list(args, 'tags')
    tags = []
    for name in tag_names:
        # If the name is not an empty string or just whitespace.
        if bool(name.strip()):
            tags.append(get_or_create(Tag, name=name))
    return tags
