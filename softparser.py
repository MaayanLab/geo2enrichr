"""This module contains functions for parsing SOFT files.

__authors__ = "Gregory Gundersen, Andrew Rouillard, Axel Feldmann, Kevin Hu"
__credits__ = "Yan Kou, Avi Ma'ayan"
__contact__ = "gregory.gundersen@mssm.edu"
"""


import os

from scipy import stats

from files import SOFTFile
from runningmean import RunningMean


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
		if platform:
			raise LookupError('Platform ' + platform + ' is not supported.')
		else:
			raise ValueError('Platform not provided.')

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
	# thinner. That said, we do not trust the DGS mapping and do the probe-to-
	# gene mapping ourselves.
	if is_gds:
		BOF = '!dataset_table_begin'
		EOF = '!dataset_table_end'
		COL_OFFSET = 2
	else:
		BOF = '!series_matrix_table_begin'
		EOF = '!series_matrix_table_end'
		COL_OFFSET = 1

	# For `dict` fast hashing to track a running mean of duplicate probe IDs.
	genes = {}

	# For statistics about data quality.
	unconverted_probes = []
	probe_count = 0

	try:
		with open(soft_file, 'r') as soft_in:
			# Skip comments.
			discard = next(soft_in)
			while discard.rstrip() != BOF:
				discard = next(soft_in)

			# Read header and set column offset.
			header = next(soft_in).rstrip('\r\n').split('\t')
			header = header[COL_OFFSET:]
			line_length = len(header)

			# Find the columns indices.
			A_incides = [header.index(gsm) for gsm in A_cols]
			B_incides = [header.index(gsm) for gsm in B_cols]

			for line in soft_in:
				split_line = line.rstrip('\r\n').split('\t')
				if split_line[0] == EOF or split_line[1] == '--Control':
					continue

				probe  = split_line[0]
				values = split_line[COL_OFFSET:]
				probe_count = probe_count + 1

				# Perform a conservative cleanup by ignoring any rows that have
				# null values or an atypical number of columns.
				if len(values) is not line_length:
					continue		
				if 'null' in values:
					continue
				# Three forward slashes, \\\, denotes multiple genes.
				if '\\\\\\' in probe:
					continue
				
				values = [float(val) for val in values]

				# GSD files already contain a column with gene symbols but we
				# do not trust that mapping.
				gene = __probe2gene(platform, probe)
				if gene is None:
					unconverted_probes.append(gene)
					continue

				if gene in genes:
					genes[gene].push(values)
				else:
					rm = RunningMean()
					rm.push(values)
					genes[gene] = rm

		conversion_pct = 100.0 - float(len(unconverted_probes)) / float(probe_count)
	except IOError:
		raise IOError('Could not read SOFT file from local server.')

	# Iterate over sybmols and values, mapping symbols to gene names if
	# necessary and putting values into A and B arrays.
	A = []
	B = []
	for gene in genes:
		# Get the final mean value of each row from each RunningMean instance.
		adj_values = genes[gene].mean()
		# Blow out the `RunningMean` instance.
		genes[gene] = adj_values
		A_row = [adj_values[i] for i in A_incides]
		B_row = [adj_values[i] for i in B_incides]
		A.append(A_row)
		B.append(B_row)

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