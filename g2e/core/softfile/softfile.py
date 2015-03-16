"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""


import core.softfile.geodownloader as geodownloader
import core.softfile.softparser as softparser
import core.softfile.normalizer as normalizer
import core.softfile.softfilemanager as softfilemanager


class SoftFile(object):

    def __init__(self, name, A_cols=None, B_cols=None, genes=None, A=None, B=None, text_file=None, is_geo=False, platform=None, stats=None):
        """Constructs a SOFT file. This should only be called via the class
        methods.
        """
        self.name = name
        self.A_cols = A_cols
        self.B_cols = B_cols
        self.genes = genes
        self.A = A
        self.B = B
        self.is_geo = is_geo
        self.platform = platform
        self.stats = stats
        self.text_file = text_file

    @classmethod
    def from_geo(cls, args):
        name = args['dataset']
        is_geo = True

        if not softfilemanager.file_exists(name):
            geodownloader.download(name)

        platform = args['platform']
        A_cols = args['A_cols'].split(',')
        B_cols = args['B_cols'].split(',')
        genes, A, B, stats = softparser.parse(name, is_geo, platform, A_cols, B_cols)
        genes, A, B = normalizer.normalize(genes, A, B)
        text_file = softfilemanager.write(name, genes, A, B)
        return cls(name, A_cols, B_cols, genes=genes, A=A, B=B, text_file=text_file, is_geo=is_geo, platform=platform, stats=stats)

    @classmethod
    def from_dao(cls, sf_dao):
        name      = sf_dao['name']
        text_file = sf_dao['text_file']
        is_geo    = sf_dao['is_geo']
        platform  = sf_dao['platform']
        return cls(name, platform=platform, text_file=text_file, is_geo=is_geo)

    @classmethod
    def from_file(cls, file_obj, args):
        name = args['name']
        text_file = softfilemanager.save(name, file_obj)
        genes, A, B = softparser.parse(name, is_geo=False)
        return cls(name, genes=genes, A=A, B=B, text_file=text_file)
