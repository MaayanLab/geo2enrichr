"""Utility methods for constructing RequiredMetadata from different user
inputs.
"""

from substrate import RequiredMetadata


def from_http_request(args):
    """Constructs a required metadata instance from HTTP request arguments.
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
