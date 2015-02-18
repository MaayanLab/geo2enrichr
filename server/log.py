"""This module contains utility functions for logging to the server.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""

DEBUG = True

def pprint(msg):
	"""Prints message in debug mode. This function makes it easy to convert
	all print statements to functions, if the application is ever moved to
	Python 3.
	"""

	if DEBUG:
		print msg