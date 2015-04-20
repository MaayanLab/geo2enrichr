import unittest

import g2e.core.targetapp.enrichr as enrichr


class TestEnrichr(unittest.TestCase):

    def testEnrichrLink(self):
        genes = [('A',1),('B',1),('C',1),('D',1),('E',1)]
        link = enrichr.get_link(genes, '')
        self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in link)
