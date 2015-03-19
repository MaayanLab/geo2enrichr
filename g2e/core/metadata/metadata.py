"""This class groups the Extraction class's various experimental metadata as
user inputs.
"""


class Metadata(object):

    def __init__(self, method, cutoff, cell, perturbation, gene, disease):
        self.method       = method
        self.cutoff       = cutoff
        self.cell         = cell
        self.perturbation = perturbation
        self.gene         = gene
        self.disease      = disease

    @classmethod
    def from_args(cls, args):
        method       = args['method']       if 'method'       in args else 'chdir'
        cutoff       = args['cutoff']       if 'cutoff'       in args else 500
        if cutoff == 'None':
            cutoff = None
        else:
            cutoff = int(cutoff)
        cell         = args['cell']         if 'cell'         in args else None
        perturbation = args['perturbation'] if 'perturbation' in args else None
        gene         = args['gene']         if 'gene'         in args else None
        disease      = args['disease']      if 'disease'      in args else None
        return cls(method, cutoff, cell, perturbation, gene, disease)

    def __str__(self):
        result = []
        for key,val in self.__dict__.items():
            result.append(str(val))
        return '-'.join(result)
