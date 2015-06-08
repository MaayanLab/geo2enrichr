import unittest

import g2e.core.targetapp.l1000cds2 as l1000cds2
from g2e.core.metadata.metadata import Metadata


class TestL1000CDS2(unittest.TestCase):

    def testL1000CDS2Link(self):
        md = Metadata(None, None, None, None, None, None, None, None, None)
        genes = [
            ('DDIT4', 9.97),
            ('HIG2', 10.16),
            ('FLT1', 7.66),
            ('ADM', 17.8),
            ('SLC2A3', 20.29),
            ('ZNF331', 15.22)
        ]
        link = l1000cds2.get_link(genes, md)
        self.assertTrue('http://amp.pharm.mssm.edu/L1000CDS2/' in link)
