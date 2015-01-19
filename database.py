"""This module handles database transactions.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sqlite3


# This connection persists for as long as the server is up and running.
# StackOverflow did not have a problem with this:
# http://stackoverflow.com/a/27829115/1830334.
conn = sqlite3.connect('database.db')


# See http://stackoverflow.com/questions/2887878.
def insert(data):
	# Use a context manager to handle exceptions and closing the connection.
	#with conn.cursor() as c:
	#	c.execute('')
	#	conn.commit()
	pass
