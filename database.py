"""This module handles database transactions.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sqlite3


# This connection persists for as long as the server is up and running.
# StackOverflow did not have a problem with this:
# http://stackoverflow.com/a/27829115/1830334.
conn = sqlite3.connect('database.db', check_same_thread=False)

COUNT_TABLE = 'ExtractionCount'


# We open and close the cursor on every transaction. I don't think this is
# highly performant, but raw speed is simply not a foreseeable issue.
def increment_extraction_count():
	cur = conn.cursor()
	cur.execute('UPDATE %s SET count = count + 1' % COUNT_TABLE)
	conn.commit()
	cur.close()
	return get_extraction_count()


def get_extraction_count():
	cur = conn.cursor()
	sql_resp = cur.execute('SELECT count FROM %s' % COUNT_TABLE)
	count = sql_resp.fetchall()[0][0]
	cur.close()
	return count


# See http://stackoverflow.com/questions/2887878.
def insert(data):
	# Use a context manager to handle exceptions and closing the connection.
	#with conn.cursor() as c:
	#	c.execute('')
	#	conn.commit()
	pass


def reset_count():
	"""Resets the counter. In theory, this should never be used. 
	"""

	cur = conn.cursor()
	cur.execute('DROP TABLE %s' % COUNT_TABLE)
	cur.execute('CREATE TABLE %s (count INTEGER PRIMARY KEY)' % COUNT_TABLE)
	cur.execute('INSERT INTO %s VALUES(0)' % COUNT_TABLE)
	conn.commit()
	cur.close()
