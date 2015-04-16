"""This module presents a single entry point, SoftFile, for creating and
fetching SOFT files. 
"""

import time

import g2e.core.softfile.geodownloader as geodownloader
import g2e.core.softfile.softparser as softparser
import g2e.core.softfile.normalizer as normalizer
import g2e.core.softfile.softfilemanager as softfilemanager


class SoftFile(object):

    def __init__(self, name, A_cols=None, B_cols=None, genes=None, A=None, B=None, text_file=None, is_geo=False, platform=None, stats=None, normalize=None):
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
        self.normalize = normalize
        self.text_file = text_file

    @classmethod
    def from_geo(cls, args):
        name = args['dataset']
        is_geo = True

        if not softfilemanager.file_exists(name):
            geodownloader.download(name)

        platform = args['platform']
        A_cols, B_cols = get_cols(args)
        genes, A, B, selections, stats = softparser.parse(name, is_geo, platform, A_cols, B_cols)

        normalize = True if ('normalize' not in args or args['normalize'] == 'True') else False
        if normalize:
            genes, A, B = normalizer.normalize(genes, A, B)

        gsms = A_cols + B_cols
        text_file = softfilemanager.write(name, platform, normalize, genes, A, B, gsms, selections, stats)
        return cls(name, A_cols, B_cols, genes=genes, A=A, B=B, text_file=text_file, is_geo=is_geo, platform=platform, stats=stats, normalize=normalize)

    @classmethod
    def from_file(cls, file_obj, args):
        name = args['name'] if 'name' in args else str(time.time())[:10]
        text_file = softfilemanager.save(name, file_obj)
        genes, A, B = softparser.parse(name, is_geo=False)
        platform = args['platform'] if 'platform' in args else None
        return cls(name, genes=genes, A=A, B=B, platform=platform, text_file=text_file)


def get_cols(args):
    """Handles getting the samples depending on the way the request was made.
    """
    # The "array[]" notation really confused me; see this Stack Overflow
    # answer for details: http://stackoverflow.com/a/23889195/1830334
    if 'A_cols[]' in args:
        A_cols = args.getlist('A_cols[]')
        B_cols = args.getlist('B_cols[]')
    elif len(args.getlist('A_cols')) > 0:
        A_cols = args.getlist('A_cols')
        B_cols = args.getlist('B_cols')
    elif 'A_cols' in args:
        A_cols = [x for x in args.get('A_cols').split(',')]
        B_cols = [x for x in args.get('B_cols').split(',')]

    A_cols = [x.encode('ascii') for x in A_cols]
    B_cols = [x.encode('ascii') for x in B_cols]

    print 'Columns selected:'
    print A_cols
    print B_cols
    return A_cols, B_cols
