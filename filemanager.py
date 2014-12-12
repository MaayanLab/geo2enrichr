"""This module builds an output file on the server.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "gregory.gundersen@mssm.edu"
"""


import cookielib
import poster
import urllib2

from files import GeneFile


def build_output_file(items, use_chdir, filename):

	full_path_up   = GeneFile(filename, 'up').full_path()
	full_path_down = GeneFile(filename, 'down').full_path()
	full_path_comb = GeneFile(filename, 'combined').full_path()

	with open(full_path_up, 'w') as up_out, open(full_path_down, 'w') as down_out, open(full_path_comb, 'w') as comb_out:
		for symbol, score in items:
			abs_score = abs(score)
			if score > 0:
				up_out.write('%s\t%f\n' % (symbol, score))
			else:
				down_out.write('%s\t%f\n' % (symbol, abs_score))
			# This file is just for Enrichr, which doesn't accept negative
			# numbers for its levels of membership. A client wouldn't want a
			# combined file without signs.
			comb_out.write('%s\t%f\n' % (symbol, abs_score))

	print "All done!"
	return {
		up: full_path_up,
		down: full_path_down,
		comb: full_path_comb
	}


def __convert_probe_IDs(list_to_convert):	
	#Step 2: Convert symbols in items
	print len(list_to_convert)
	converted_items = []
	unable_to_convert_list = []
	total_probe_ID = []
	for probe, pvalue in list_to_convert:
		if '"' in probe or "'" in probe:
			probe = probe[1:-1] #to strip quotes, assuming there are quotes

		if probe in PROBE2GENE:
			converted_items.append((PROBE2GENE[probe], pvalue))
		else:
			unable_to_convert_list.append(probe)
		total_probe_ID.append(probe)
	try:
		conversion_percent = float(len(converted_items))/float(len(total_probe_ID))
	except:
		conversion_percent = 0
	
	read_out = 'We tried to match {0} probes, but could only convert {1} of them, and could not convert {2}\
	of them. That is a success rate of {3}'.format(len(total_probe_ID), len(converted_items),\
	len(unable_to_convert_list), conversion_percent)

	return (converted_items, read_out)



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


PROBE2GENE = __open_probe_dict('static/probe2gene.txt')