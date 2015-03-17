"""This class groups the Extraction class's various experimental metadata as
user inputs.
"""


class Metadata(object):

    def __init__(self, method, cutoff):
        self.method = method
        self.cutoff = cutoff
