# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


"""SOFT Util

SOFT Util is the entry-point for the following steps:
1. Using specified accession numbers from manual literature searches,
download SOFT files from GEO.
2. Once downloaded, parse these files to calculate the differentially
expressed gene lists.
3. Generate GMT--Where is this done?
"""


import os
import re
import pdb

import geofetcher
import geoparser
import util


#accessionlist is a .txt filename with accession numbers as columns
def process_file(accessionlist, use_chdir=False, getFuzzy=False):
	#probe_2_symbol_dict = open_probe_dict("Probe_2_Symbol_Unique.txt")
	with open(accessionlist, 'r') as f:
		#with open("Supported_Platforms_186_07_18_2013.txt") as g:
		#    platform_list = []
		#    for row in g:
		#        split_row = row.rstrip().split('\t')
		#        platform_list.append(split_row[0])
		
		chdir, list_folder = util.get_directories(use_chdir)

		print "Starting on first entries"

		for i, row in enumerate(f):
			#if i < 1:
			#    continue
			#Step 1 Process Text from Accession List.
			
			#platform = split_row[6]
			#if platform not in platform_list:
			#   continue

			#Make sure the following variable assignments make sense with your data table
			split_row = row.rstrip().split('\t')
			accession_num = split_row[0].upper()
			species = split_row[5]
			platform = split_row[4].upper()
			TF_name = split_row[1]
			control = split_row[2].split(',')
			experimental = split_row[3].split(',')

			process_request(accession_num, species, platform, TF_name, control, experimental, chdir, list_folder, use_chdir, getFuzzy)


def process_request(accession_num, species, platform, TF_name, control, experimental, chdir, list_folder, use_chdir, getFuzzy):
	if len(control) > 2 and len(experimental) > 2:
		if 'GSE' in accession_num:
			control = ['"{}"'.format(x.upper()) for x in control]
			experimental = ['"{}"'.format(x.upper()) for x in experimental]
		else:
			control = [x.upper() for x in control]
			experimental = [x.upper() for x in experimental]
		
		annotation_info = '{0}_{1}_{2}'.format(TF_name, species, platform)
		print annotation_info
		print control, experimental

		constructed_filename = annotation_info + '_' + accession_num
		print "Okay, so filenames have been assigned, and the row has been split up!"

		# skip files already analyzed
		#if '{0}{1}_up_genes.txt'.format(constructed_filename, chdir) in os.listdir('{0}\\{1}'.format(os.getcwd(), list_folder)):
		#	print 'Already analyzed {}'.format(constructed_filename)
		#	#continue
		#	return

		# skip these files because they are exceptions
		exception_list = []
		if annotation_info in exception_list:
			#continue
			return

		if 'GDS' in accession_num:
			print "Now getting the SOFT file."
			#Step 2 Pass this information to the SOFT getter.
			geofetcher.getSOFTFile(accession_num, list_folder, annotation_info)
			
			print "Now analyzing the SOFT file..."
			#Step 3 Tell the parser to go.
			#Step_3_GEO_ParserUPDOWNGENELISTS.parse_soft(list_folder + constructed_filename + '.soft', probe_2_symbol_dict, use_chdir, getFuzzy, control_names = control, experimental_names = experimental)
			filenames = geo_parser.parse_soft(list_folder + constructed_filename + '.soft', probe_2_symbol_dict, use_chdir, getFuzzy, control_names=control, experimental_names=experimental)
			os.remove(list_folder + constructed_filename + '.soft')
			print annotation_info
			return filenames

		else:
			print "Now getting the Series Matrix file..."
			#Step 2 Pass this information to the Series_Matrix getter.
			geofetcher.getSeriesMatrixFile(accession_num, platform, list_folder, annotation_info)

			print "Now analyzing the Series Matrix file..."
			#Step 3 Tell the parser to go.
			#Step_3_GEO_ParserUPDOWNGENELISTS.parse_series_matrix(list_folder + constructed_filename + '.txt', probe_2_symbol_dict, use_chdir, getFuzzy, control_names = control, experimental_names = experimental)
			filenames = geo_parser.parse_series_matrix(list_folder + constructed_filename + '.txt', probe_2_symbol_dict, use_chdir, getFuzzy, control_names=control, experimental_names=experimental)
			os.remove(list_folder + constructed_filename + '.txt')
			print annotation_info
			return filenames


probe_2_symbol_dict = util.open_probe_dict("Probe_2_Symbol_Unique.txt")