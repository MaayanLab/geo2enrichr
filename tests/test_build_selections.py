import unittest

from g2e.signaturefactory.softfileutils.filemanager import _build_selections


class TestBuildSelections(unittest.TestCase):

	def testAABB(self):
		selections = {}
		selections['a_indices'] = [0,1]
		selections['b_indices'] = [2,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['a','a','b','b'])

	def testABAB(self):
		selections = {}
		selections['a_indices'] = [0,2]
		selections['b_indices'] = [1,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['a','b','a','b'])

	def testBABA(self):
		selections = {}
		selections['a_indices'] = [2,4]
		selections['b_indices'] = [1,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['b','a','b','a'])

	def testBBABBBB(self):
		selections = {}
		selections['a_indices'] = [3]
		selections['b_indices'] = [1,2,4,5,6,7]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['b','b','a','b','b','b','b'])

	def testIndices(self):
		selections = {}
		selections['a_indices'] = [3,99]
		selections['b_indices'] = [45,67]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['a','b','b','a'])
