"""This module handles database transactions.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sqlite3


# This connection persists for as long as the server is up and running.
# StackOverflow did not have a problem with this:
# http://stackoverflow.com/a/27829115/1830334.
conn = sqlite3.connect('euclid.db', check_same_thread=False)

# We open and close the cursor on every transaction. I don't think this is
# highly performant, but raw speed is simply not a foreseeable issue.


EXTRACTION_TABLE    = 'Extractions'
# TODO: I have been referring to the experiment accession number as *the*
# "accession" but in fact the platform and sample IDs are also accessions.
# This should be properly renamed throughout the codebase.
EXPERIMENT_TABLE    = 'Experiments'
PLATFORM_TABLE      = 'Platforms'
SAMPLE_TABLE        = 'Samples'
RARE_DISEASES_TABLE = 'RareDiseases'

# Junction table to map an Extraction ID to a Sample ID.
SELECTED_SAMPLES_TABLE = 'SelectedSamples'

# Cache the rare disease list in memory so we do not make this call on every
# GEO2Enrichr instance.
cur = conn.cursor()
cur.execute('SELECT * FROM %s' % RARE_DISEASES_TABLE)
RARE_DISEASES_LIST = [x[1] for x in cur.fetchall()]
cur.close()


# See http://stackoverflow.com/questions/2887878.
def record_extraction(accession, platform, organism, A, B, metadata=None):
	cur = conn.cursor()

	# Insert the experiment ID and platform into their respective tables;
	# these queries should create the data if it does not already exist. We
	# store the transaction IDs in order to build the query for the extraction
	# table.
	cur.execute('INSERT INTO %s VALUES("%s");' % (EXPERIMENT_TABLE, accession))
	experiment_id = cur.lastrowid

	cur.execute('INSERT INTO %s VALUES("%s");' % (PLATFORM_TABLE, platform))
	platform_id = cur.lastrowid

	# Record extraction event.
	cur.execute('INSERT INTO %s VALUES(NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s");' %\
		(EXTRACTION_TABLE, experiment_id, platform_id, organism, 'chdir', 'cell', '', 'gene'))
	extraction_id = cur.lastrowid

	# Map the newly created "extraction_id" to every sample the user selected.
	for control in (A + B):
		cur.execute('INSERT INTO %s VALUES("%s");' % (SAMPLE_TABLE, control))
		cur.execute('INSERT INTO %s VALUES("%s", "%s");' % (SELECTED_SAMPLES_TABLE, extraction_id, control))

	conn.commit()
	cur.close()


def get_extraction_count():
	"""Returns the number of gene lists that have been extracted from GEO.
	"""

	cur = conn.cursor()
	cur.execute('SELECT Count(*) FROM %s;' % EXTRACTION_TABLE)
	return cur.fetchone()[0]


def get_rare_diseases():
	"""Returns a list of rare diseases.
	"""

	return RARE_DISEASES_LIST


def reset_database():
	"""Resets the database for testing.
	"""

	cur = conn.cursor()
	
	# Blow out the database.
	cur.execute('DROP TABLE IF EXISTS %s;' % PLATFORM_TABLE)
	cur.execute('DROP TABLE IF EXISTS %s;' % EXPERIMENT_TABLE)
	cur.execute('DROP TABLE IF EXISTS %s;' % SAMPLE_TABLE)
	cur.execute('DROP TABLE IF EXISTS %s;' % EXTRACTION_TABLE)
	cur.execute('DROP TABLE IF EXISTS %s;' % SELECTED_SAMPLES_TABLE)
	cur.execute('DROP TABLE IF EXISTS %s;' % RARE_DISEASES_TABLE)

	# Rebuild the tables.
	cur.execute('CREATE TABLE %s(Accession TEXT);' % PLATFORM_TABLE)
	cur.execute('CREATE TABLE %s(Accession TEXT);' % EXPERIMENT_TABLE)
	cur.execute('CREATE TABLE %s(Accession TEXT);' % SAMPLE_TABLE)
	cur.execute('''CREATE TABLE %s(
			Id INTEGER PRIMARY KEY,
			Accession TEXT,
			Platform TEXT,
			Organism TEXT,
			DiffExpMethod TEXT,
			Cell TEXT,
			Perturbation TEXT,
			Gene TEXT)''' % EXTRACTION_TABLE)
	cur.execute('CREATE TABLE %s(ExtractionId INTEGER, Accession TEXT);' % SELECTED_SAMPLES_TABLE)
	
	# Setup the rare diseases table.
	cur.execute('CREATE TABLE %s(Id INTEGER PRIMARY KEY, Name TEXT);' % RARE_DISEASES_TABLE) 
	with open('resources/all-rare-diseases.txt') as ds:
		for line in ds:
			line = line.replace('\n', '')
			if line == '':
				continue
			cur.execute('INSERT INTO %s VALUES(NULL, "%s");' % (RARE_DISEASES_TABLE, line))

	conn.commit()
	cur.close()


if __name__ == '__main__':
	get_rare_diseases()
