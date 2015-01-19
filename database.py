"""This module handles database transactions.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sqlite3


def insert(data):
	# Should I open a connection on every insert?
	#conn = sqlite3.connect('database.db')
	# Use the context manager to handle exceptions and closing the connection.
	# See http://stackoverflow.com/a/27829115/1830334.
	#with conn.cursor() as c:
	#	c.execute('')
	#	conn.commit()
	pass
