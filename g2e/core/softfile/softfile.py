"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""


import g2e.core.softfile.geodownloader as geodownloader
import g2e.core.softfile.softparser as softparser
import g2e.core.softfile.normalizer as normalizer
import g2e.core.softfile.softfilemanager as softfilemanager


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
        # The "array[]" notation really confused me; see this Stack Overflow
        # answer for details: http://stackoverflow.com/a/23889195/1830334
        import pdb; pdb.set_trace()
        A_cols = args.getlist('A_cols[]') or args.getlist('A_cols')
        B_cols = args.getlist('B_cols[]') or args.getlist('B_cols')
        genes, A, B, stats = softparser.parse(name, is_geo, platform, A_cols, B_cols)
        genes, A, B = normalizer.normalize(genes, A, B)
        text_file = softfilemanager.write(name, genes, A, B)
        return cls(name, A_cols, B_cols, genes=genes, A=A, B=B, text_file=text_file, is_geo=is_geo, platform=platform, stats=stats)

    @classmethod
    def from_file(cls, file_obj, args):
        name = args['name']
        text_file = softfilemanager.save(name, file_obj)
        genes, A, B = softparser.parse(name, is_geo=False)
        return cls(name, genes=genes, A=A, B=B, text_file=text_file)
