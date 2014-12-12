"""This module contains functions for parsing SOFT files.

__authors__ = "Gregory Gundersen, Andrew Rouillard, Axel Feldmann, Kevin Hu"
__credits__ = "Yan Kou, Avi Ma'ayan"
__contact__ = "gregory.gundersen@mssm.edu"
"""


import os

from scipy import stats

from files import SOFTFile
from runningstat import RunningStat


def parse(filename, platform, A_cols, B_cols):
	"""Parses SOFT files, discarding bad data, averaging duplicates, and
	converting probe IDs to gene sybmols.
	"""

	# NOTE: This is the most complicated function in the program. It is
	# mission critical that this function works as expected, parsing,
	# cleaning, and averaging the data correctly.

	# Yan Kou recommended using pandas: http://pandas.pydata.org/.
	# Her pseudocode was:
	#
	#     import pandas as pd
	#     data = pd.DataFrame('yourfile.txt')
	#     gdata = data.groupby('column1').mean()

	# Premature optimization is the root of all evil, but it is worth noting
	# that this function's running time is ~2N+C, where N is the number of
	# lines in the table and C is the number of comment lines. It would be
	# ideal if we did not loop over the table lines twice.

	if platform not in PROBE2GENE:
		raise LookupError('Platform ' + platform + ' is not supported.')

	soft_file = SOFTFile(filename).path()
	is_gds = 'GDS' in filename
	if is_gds:
		A_cols = [x.upper() for x in A_cols]
		B_cols = [x.upper() for x in B_cols]
	else:
		A_cols = ['"{}"'.format(x.upper()) for x in A_cols]
		B_cols = ['"{}"'.format(x.upper()) for x in B_cols]

	# COL_OFFSET changes because GDS files are "curated", meaning that they
	# have their gene symbols included. GSE files do not and are 1 column
	# thinner.
	if is_gds:
		BOF = '!dataset_table_begin'
		EOF = '!dataset_table_end'
		COL_OFFSET = 1
	else:
		BOF = '!series_matrix_table_begin'
		EOF = '!series_matrix_table_end'
		COL_OFFSET = 0

	# For `dict` fast hashing to track a running mean of duplicate probe IDs.
	genes_dict = {}

	# For statistics about data quality.
	null_probes = []
	unconverted_probes = []

	try:
		with open(soft_file) as soft_in:
			# Skip comments.
			discard = next(soft_in)
			while discard.rstrip() != BOF:
				discard = next(soft_in)
			
			# Read header and set column offset.
			header = next(soft_in).rstrip('\r\n').split('\t')
			header = header[COL_OFFSET+1:]
			line_length = len(header)

			# Find the columns indices.
			A_incides = [header.index(gsm) for gsm in A_cols]
			B_incides = [header.index(gsm) for gsm in B_cols]

			for line in soft_in:
				split_line = line.rstrip('\r\n').split('\t')
				if split_line[0] == EOF or split_line[1] == '--Control':
					continue

				symbol = split_line[COL_OFFSET]
				values = split_line[COL_OFFSET+1:]
		
				# Perform a conservative cleanup by ignoring any rows that have
				# null values or an atypical number of columns.
				if 'null' in values:
					null_probes.append((symbol, values))
					continue
				if len(values) is not line_length:
					continue

				values = [float(val) for val in values]
				if symbol in genes_dict:
					genes_dict[symbol].push(values)
				else:
					rs = RunningStat()
					rs.push(values)
					genes_dict[symbol] = rs
	except IOError:
		raise IOError('Could not read SOFT file from local server.')

	# Iterate over sybmols and values, mapping symbols to gene names if
	# necessary and putting values into A and B arrays.
	A = []
	B = []
	genes = []

	for symbol in genes_dict:
		# Get the final mean value of each row from each RunningStat instance.
		adj_values = genes_dict[symbol].mean()
		A_row = [adj_values[i] for i in A_incides]
		B_row = [adj_values[i] for i in B_incides]

		# GSD files already contain a column with gene symbols and do not need
		# to be converted.
		if is_gds:
			A.append(A_row)
			B.append(B_row)
			genes.append(symbol)
		else:
			symbol = __probe2gene(platform, symbol)
			if symbol is None:
				unconverted_probes.append(symbol)
				continue
			else:
				A.append(A_row)
				B.append(B_row)
				genes.append(symbol)

	conversion_pct = 100.0 - float(len(unconverted_probes)) / float(len(genes_dict.keys()))
	return (A, B, genes, conversion_pct)


def __probe2gene(platform, probe):
	"""Converts probe IDs to gene symbols. Does not check if the platform is
	supported.
	"""

	# Strip any potential quotation marks.
	probe = probe.replace('"', '').replace('\'', '')
	try:
		if probe in PROBE2GENE[platform]:
			return PROBE2GENE[platform][probe]
	except AttributeError:
		return None
	return None


def __open_probe_dict(platform_probesetid_genesym_file):
	"""Platform data collected and script written by Andrew Rouillard.
	"""

	platformdictionary = {}
	with open(platform_probesetid_genesym_file) as f:
		for line in f:
			entries = line.rstrip().split('\t')
			platform = entries[0]
			probesetid = entries[1]
			genesym = entries[2]
			if platform in platformdictionary:
				platformdictionary[platform][probesetid] = genesym
			else:
				platformdictionary[platform] = {probesetid:genesym}
	return platformdictionary


# This loads a ~300MB Python dictionary into memory. Is there a better way to
# do this?
PROBE2GENE = __open_probe_dict('static/probe2gene.txt')