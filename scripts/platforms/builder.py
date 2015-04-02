def build_probe_dict(platform_probesetid_genesym_file):
    """Builds an in-memory dictionary mapping platforms to probe IDs to gene
    symbols.
    """
    # Platform data collected and script written by Andrew Rouillard.
    platform_dict = {}
    with open(platform_probesetid_genesym_file) as f:
        for line in f:
            entries = line.rstrip().split('\t')
            platform = entries[0]
            probesetid = entries[1]
            genesym = entries[2]
            if platform in platform_dict:
                platform_dict[platform][probesetid] = genesym
            else:
                platform_dict[platform] = {probesetid:genesym}
    return platform_dict


PROBE2GENE = build_probe_dict('../../g2e/core/softfile/probe2gene.txt')
