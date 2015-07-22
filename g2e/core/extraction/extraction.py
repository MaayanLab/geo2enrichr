"""Creates an Extraction, which represents a single instance of a user's
processed data, with links to the SOFT file, gene lists, and metadata.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import hashlib
import time

from g2e.core.softfile.softfile import SoftFile
from g2e.core.metadata.metadata import Metadata
from g2e.core.genelist.genelistsmaker import genelists_maker


class Extraction(object):

    def __init__(self, softfile, genelists, metadata):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        # This is *not* the database ID. This is hashed so that users cannot
        # simply guess the ID for other user's data.
        self.extraction_id = hashlib.sha1(str(time.time())).hexdigest()[:10]
        self.softfile  = softfile
        self.genelists = genelists
        self.metadata  = metadata

    @classmethod
    def new(cls, softfile, args):
        """Creates a new extraction, as opposed to an extraction from the
        database.
        """
        metadata = Metadata.from_args(args)
        skip_target_apps = True if 'skip_targets_apps' in args else False
        genelists = genelists_maker(softfile, metadata, skip_target_apps)
        return cls(softfile, genelists, metadata)

    @classmethod
    def from_geo(cls, args):
        """Creates an extraction from GEO data.
        """
        softfile = SoftFile.from_geo(args)
        return cls.new(softfile, args)

    @classmethod
    def from_file(cls, file_obj, args):
        """Creates an extraction from a custom, uploaded SOFT file.
        """
        # PURPLE_WIRE: Users *will* upload bad data and parsing their files
        # *will* throw an error. Catch and handle appropriately.
        softfile = SoftFile.from_file(file_obj, args)
        return cls.new(softfile, args)
