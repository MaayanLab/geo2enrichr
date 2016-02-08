import unittest

import g2e.targetapps.crowdsourcing as crowdsourcing
from substrate import Gene, GeoDataset, OptionalMetadata, RankedGene,\
    SoftFile, SoftFileSample, Tag


class TestCrowdsourcing(unittest.TestCase):

    def setUp(self):

        self.optional_metadata = [
            OptionalMetadata('cell_type', 'foo'),
            OptionalMetadata('organism', 'foo'),

            OptionalMetadata('young', 'foo'),
            OptionalMetadata('old', 'foo'),
            OptionalMetadata('age_unit', 'foo'),

            OptionalMetadata('microbe_name', 'foo'),
            OptionalMetadata('microbe_id', 'foo'),
        ]

        self.samples = [SoftFileSample(name, False) for name in ['a2','a2','a3']]

        self.genes = [
            RankedGene(Gene('DDIT4'), 9.97),
            RankedGene(Gene('HIG2'), 10.16),
            RankedGene(Gene('FLT1'), 7.66),
            RankedGene(Gene('ADM'), -17.8),
            RankedGene(Gene('SLC2A3'), -20.29),
            RankedGene(Gene('ZNF331'), -15.22)
        ]

        dataset = GeoDataset(
            accession='XXX',
            title='fake_title',
            platform='fake_platform'
        )
        self.soft_file = SoftFile(self.samples, dataset, self.genes, None, None, False)

    def testWithOneTag(self):
        self.optional_metadata += [
            OptionalMetadata('user_key', '52354fa2e3f22a788f82b6634a5ad548')
        ]

        tag_name = 'AGING_BD2K_LINCS_DCIC_COURSERA'
        tags = [Tag(tag_name)]

        link = crowdsourcing.get_link(
            self.genes, self.optional_metadata, self.soft_file, tags
        )

        self.assertTrue(
            link,
            'http://maayanlab.net/crowdsourcing/microtask_leaderboard.php#task5'
        )