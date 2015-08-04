"""Groups the Extraction class's various experimental metadata as user inputs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


class Metadata(object):

    def __init__(self, diffexp_method, cutoff, correction_method, threshold, organism, cell, perturbation, gene, disease, platform=None, normalize=None):
        """Constructs a Metadata instance.
        """
        self.diffexp_method    = diffexp_method
        self.correction_method = correction_method
        self.cutoff            = cutoff
        self.threshold         = threshold
        self.organism          = organism
        self.cell              = cell
        self.perturbation      = perturbation
        self.gene              = gene
        self.disease           = disease
        self.platform          = platform
        self.normalize         = normalize

    @classmethod
    def from_args(cls, args):
        """Constructs a metadata instance from arguments as opposed to the
        database.
        """
        diffexp_method = args['diffexp_method'] if 'diffexp_method' in args else 'chdir'
        
        # This if-else-iness smells, but I'm not sure what else to do right
        # now. There has to be a better way to handle user input, right?
        if diffexp_method == 'chdir':
            cutoff = args['cutoff'] if 'cutoff' in args else 500
            correction_method = 'NA'
            threshold = None
            if cutoff == 'none' or cutoff == 'None':
                cutoff = None
            else:
                cutoff = int(cutoff)
        else:
            cutoff = None
            correction_method = args['correction_method'] if 'correction_method' in args else 'BH'
            if correction_method == 'none' or correction_method == 'None':
                correction_method = None
                threshold = None
            else:
                threshold = args['threshold'] if 'threshold' in args else 0.01
                if threshold == 'none' or threshold == 'None':
                    threshold = None
                else:
                    threshold = float(threshold)

        organism     = args['organism']     if 'organism'     in args else None
        cell         = args['cell']         if 'cell'         in args else None
        perturbation = args['perturbation'] if 'perturbation' in args else None
        gene         = args['gene']         if 'gene'         in args else None
        disease      = args['disease']      if 'disease'      in args else None

        # This metadata is actually in the SoftFile instance as well, but
        # adding it here makes it easier to add to the description passed to
        # the target applications.
        platform     = args['platform']     if 'platform'     in args else None
        normalize    = True if ('normalize' not in args or args['normalize'] == 'True') else False
        return cls(diffexp_method, cutoff, correction_method, threshold, organism, cell, perturbation, gene, disease, platform, normalize)

    @classmethod
    def from_extraction(cls, extraction):

        if extraction.diff_exp_method:
            diff_exp_method = extraction.diff_exp_method.name
        else:
            diff_exp_method = None

        if (extraction.ttest_correction_method):
            ttest_correction_method = extraction.ttest_correction_method.name
        else:
            ttest_correction_method = None

        return cls(
            diff_exp_method,
            extraction.cutoff,
            ttest_correction_method,
            extraction.threshold,
            extraction.organism,
            extraction.cell,
            extraction.perturbation,
            extraction.gene,
            extraction.disease
        )

    def __str__(self):
        """Stringifies the metadata instance.
        """
        # This is used primarily for sending a description to third-party
        # target applications.
        result = []
        for key,val in self.__dict__.items():
            if val:
                result.append(str(val))
        return '-'.join(result)

    def to_L1000CDS2_data_format(self):
        result = []
        for key,val in self.__dict__.items():
            result.append({
                'key': key,
                'value': val
            })
        return result
