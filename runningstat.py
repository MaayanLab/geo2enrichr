"""This module contains a single class, `RunningStat`, which is useful for
tracking statistics about data on a single pass.

See http://www.johndcook.com/blog/standard_deviation/

__authors__ = "Gregory Gundersen"
__credits__ = "Andrew Rouillard"
__contact__ = "avi.maayan@mssm.edu"
"""


import numpy as np


class RunningStat:


	def __init__(self):
		self.N = 0
		self.old_mean = None
		self.new_mean = None


	def push(self, values):
		# Track the number of items added to this class.
		self.N = self.N + 1
		if (self.N == 1):
			self.old_mean = self.new_mean = np.array(values)
		else:
			# See http://math.stackexchange.com/a/22351/159872 for a
			# mathematical derivation.
			self.new_mean = self.old_mean + ((values - self.old_mean) / self.N)
			self.old_mean = self.new_mean


	def mean(self):
		if self.old_mean is not None:
			return self.old_mean
		return 0


if __name__ == '__main__':
	a = np.array([1.0,1.0,1.0])
	b = np.array([2.0,2.0,2.0])
	c = np.array([3.0,6.0,3.0])

	rs = RunningStat()
	rs.push(a)
	print rs.mean()
	rs.push(b)
	print rs.mean()
	rs.push(c)
	print rs.mean()