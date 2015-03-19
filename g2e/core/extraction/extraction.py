"""This module creates an Extraction instance.
"""


from core.softfile.softfile import SoftFile
from core.metadata.metadata import Metadata
from core.genelist.genelistsmaker import genelists_maker


class Extraction(object):

    def __init__(self, softfile, genelists, metadata):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        self.softfile  = softfile
        self.genelists = genelists
        self.metadata  = metadata

    @classmethod
    def new(cls, softfile, args):
        metadata = Metadata.from_args(args)
        genelists = genelists_maker(softfile, metadata)
        return cls(softfile, genelists, metadata)

    @classmethod
    def from_geo(cls, args):
        softfile = SoftFile.from_geo(args)
        return cls.new(softfile, args)

    @classmethod
    def from_file(cls, file_obj, args):
        # PURPLE_WIRE: Users *will* upload bad data and parsing their files
        # *will* throw an error. Catch and handle appropriately.
        softfile = SoftFile.from_file(file_obj, args)
        return cls.new(softfile, args)
