"""Utility methods for constructing Tags from user input.
"""

from g2e.database.utils import get_or_create
from g2e.endpoints.request_utils import get_param_as_list
from substrate import Tag


def from_http_request(args):
    """Returns list of Tag instances.
    """
    tag_names = get_param_as_list(args, 'tags')
    tags = []
    for name in tag_names:
        # If the name is not an empty string or just whitespace.
        if bool(name.strip()):
            tags.append(get_or_create(Tag, name=name))
    return tags
