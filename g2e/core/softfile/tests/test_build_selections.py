import unittest
import numpy as np

from g2e.core.softfile.softfilemanager import _build_selections


class TestBuildSelections(unittest.TestCase):

	def testAABB(self):
		selections = {}
		selections['A_indices'] = [0,1]
		selections['B_indices'] = [2,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['A','A','B','B'])

	def testABAB(self):
		selections = {}
		selections['A_indices'] = [0,2]
		selections['B_indices'] = [1,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['A','B','A','B'])

	def testBABA(self):
		selections = {}
		selections['A_indices'] = [2,4]
		selections['B_indices'] = [1,3]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['B','A','B','A'])

	def testBBABBBB(self):
		selections = {}
		selections['A_indices'] = [3]
		selections['B_indices'] = [1,2,4,5,6,7]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['B','B','A','B','B','B','B'])

	def testIndices(self):
		selections = {}
		selections['A_indices'] = [3,99]
		selections['B_indices'] = [45,67]
		ans = _build_selections(selections)
		self.assertEqual(ans, ['A','B','B','A'])
