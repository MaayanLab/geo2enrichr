"""
"""


import time

from substrate import CustomDataset, GeoDataset, SoftFile, SoftFileSample

from g2e.util.requestutil import get_param_as_list
from g2e.core.softfile import softfileparser, softcleaner, softfilemanager
from g2e.db.util import get_or_create
from g2e.db import dataaccess


def from_geo(args):
    """Constructs a SoftFile
    """
    accession = args['dataset']

    if not softfilemanager.file_exists(accession):
        softfilemanager.download(accession)

    dataset = dataaccess.get_dataset(accession)
    if dataset == None:
        platform = args['platform']
        if platform.index('GPL') == 0:
            platform = platform[3:]
        organism = args['organism'] if 'organism' in args else 'TODO'
        title = args['title']       if 'title'    in args else 'TODO'
        summary = args['summary']   if 'summary'  in args else 'TODO'
        dataset = GeoDataset(
            accession=accession,
            platform=platform,
            organism=organism,
            title=title,
            summary=summary
        )
    else:
        print 'Dataset %s already exists!' % accession

    a_cols = get_param_as_list(args, 'A_cols')
    b_cols = get_param_as_list(args, 'B_cols')

    # Use get_or_create to track GSMs. We don't do this for custom files.
    control      = [get_or_create(SoftFileSample, name=sample, is_control=True)  for sample in a_cols]
    experimental = [get_or_create(SoftFileSample, name=sample, is_control=False) for sample in b_cols]
    samples = control + experimental

    genes, a_vals, b_vals, selections, stats = softfileparser.parse(accession, True, dataset.platform, samples)
    normalize = True if ('normalize' not in args or args['normalize'] == 'True') else False
    genes, a_vals, b_vals = softcleaner.clean(genes, a_vals, b_vals, normalize)

    text_file = softfilemanager.write(accession, dataset.platform, normalize, genes, a_vals, b_vals, samples, selections, stats)

    return SoftFile(
        samples, dataset, text_file,
        genes, a_vals, b_vals,
        stats=stats, normalize=normalize
    )


def from_file(file_obj, args):
    """Constructs a SoftFile from a user uploaded file.
    """
    # We support name and title for historical reasons, i.e. Firefox
    # support since we won't be releasing new versions of the add on.
    if 'name' in args and args['name'] != '':
        title = args['name']
    elif 'title' in args and args['title'] != '':
        title = args['title']
    else:
        title = str(time.time())[:10]

    text_file = softfilemanager.save(title, file_obj)
    genes, a_vals, b_vals, samples = softfileparser.parse(title, is_geo=False)

    control =      [SoftFileSample(x[0], True)  for x in samples if x[1] == '0']
    experimental = [SoftFileSample(x[0], False) for x in samples if x[1] == '1']
    samples = control + experimental

    organism = args['organism'] if 'organism' in args else None

    dataset = CustomDataset(
        title=title,
        organism=organism
    )
    return SoftFile(samples, dataset, text_file, genes, a_vals, b_vals)
