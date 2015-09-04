import unittest

import g2e.core.targetapp.crowdsourcing as crowdsourcing
from g2e.model.optionalmetadata import OptionalMetadata
from g2e.model.gene import Gene
from g2e.model.rankedgene import RankedGene
from g2e.model.softfile import SoftFile
from g2e.model.softfilesample import SoftFileSample
from g2e.model.tag import Tag


class TestCrowdsourcing(unittest.TestCase):

    def setUp(self):
        self.optional_metadata = [
            OptionalMetadata('pert_id', 'foo'),
            OptionalMetadata('pert_name', 'foo'),
            OptionalMetadata('gene', 'foo'),
            OptionalMetadata('cell_type', 'foo'),
            OptionalMetadata('organism', 'foo'),
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

        self.soft_file = SoftFile('fake_name', self.samples, [], None, None, 'fake_platform', None)

    def testWithOneTag(self):
        # I could create a new email address for this, but I don't really care.
        self.optional_metadata += [
            OptionalMetadata('user_email', 'greg@c4q.nyc'),
            OptionalMetadata('user_key', '52354fa2e3f22a788f82b6634a5ad548')
        ]

        tag_name = 'AGING_BD2K_LINCS_DCIC_COURSERA'
        tags = [Tag(tag_name)]
        response = crowdsourcing.post_if_necessary(
            self.genes, self.optional_metadata, self.soft_file, tags
        )
        self.assertTrue(
            response[tag_name],
            'http://maayanlab.net/crowdsourcing/microtask_leaderboard.php#task5'
        )

    def testWithTwoTags(self):
        # I could create a new email address for this, but I don't really care.
        self.optional_metadata += [
            OptionalMetadata('user_email', 'greg@c4q.nyc'),
            OptionalMetadata('user_key', '52354fa2e3f22a788f82b6634a5ad548')
        ]

        tag_name_1 = 'AGING_BD2K_LINCS_DCIC_COURSERA'
        tag_name_2 = 'PATHOGENS_BD2K_LINCS_DCIC_COURSERA'
        tags = [Tag(tag_name_1), Tag(tag_name_2)]
        response = crowdsourcing.post_if_necessary(
            self.genes, self.optional_metadata, self.soft_file, tags
        )
        self.assertTrue(
            response[tag_name_1],
            'http://maayanlab.net/crowdsourcing/microtask_leaderboard.php#task5'
        )
        self.assertTrue(
            response[tag_name_2],
            'http://maayanlab.net/crowdsourcing/microtask_leaderboard.php#task7'
        )

    def testErrorHandling(self):
        tag_name = 'AGING_BD2K_LINCS_DCIC_COURSERA'
        tags = [Tag(tag_name)]
        response = crowdsourcing.post_if_necessary(
            self.genes, self.optional_metadata, self.soft_file, tags
        )
        self.assertEqual(response['message'], 'Authentication Failed.')