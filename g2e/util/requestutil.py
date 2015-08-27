"""Utility methods for HTTP requests.
"""


def get_param_as_list(args, param):
    """Handles getting the samples depending on the way the HTTP request was
    made.
    """
    # The "array[]" notation really confused me; see this Stack Overflow
    # answer for details: http://stackoverflow.com/a/23889195/1830334
    param_brackets = param + '[]'
    if param_brackets in args:
        result = args.getlist(param_brackets)
    elif len(args.getlist(param)) > 1:
        result = args.getlist(param)
    elif param in args:
        result = [x for x in args.get(param).split(',')]
    else:
        result = []
    result = [x.encode('ascii') for x in result]
    return result
