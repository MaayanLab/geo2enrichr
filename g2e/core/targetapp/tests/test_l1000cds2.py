import unittest

import g2e.core.targetapp.l1000cds2 as l1000cds2


class TestL1000CDS2(unittest.TestCase):

    def testL1000CDS2Link(self):
        genes = [
            ('USP18', -0.10536861617612463),
            ('H19', 0.0979803999370785),
            ('COL3A1', 0.09012118037674563),
            ('MYL9', 0.09001543082469686),
            ('CTGF', 0.08922812355076926),
            ('TAGLN', 0.0823789311253236)
        ]
        link = l1000cds2.get_link(genes)
        self.assertTrue('http://amp.pharm.mssm.edu/L1000CDS2/' in link)
