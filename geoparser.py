# -----------------------------------------------------------------------------
# <credits, etc.>
# -----------------------------------------------------------------------------


import os

from scipy import stats


def parse_soft_file(full_path, control_names, experimental_names, BOF, EOF, header_index):
	# Why do we save the probes?
	removed_probes = []
	pvalues = []

	# chdir variables
	gene_order = []
	control = []
	experimental = []

	with open(full_path) as soft_file:
		# skip comments
		discard = next(soft_file)
		while discard.rstrip() != BOF:
			discard = next(soft_file)
		
		# read header
		header = next(soft_file)
		header = header.rstrip('\r\n').split('\t')
		header = header[header_index+1:]

		# find the columns indices
		control_indices = [header.index(gsm) for gsm in control_names]
		experimental_indices = [header.index(gsm) for gsm in experimental_names]

		counter = 0
		# read rest of soft
		for line in soft_file:
			counter += 1
			if counter % 1000 == 0:
				# GWG: This could be the source of server sent events?
				print counter

			split_line = line.rstrip('\r\n').split('\t')
			if split_line[0] == EOF or split_line[1] == '--Control':
				continue

			symbol = split_line[header_index]
			values = split_line[header_index+1:]

			if 'null' in values:
				removed_probes.append((symbol, values))
				continue

			try:
				control_values = [float(values[i]) for i in control_indices]
				experimental_values = [float(values[i]) for i in experimental_indices]
			except ValueError:
				continue

			# always perform ttest
			# TODO: This isn't really parsing. This is an analytical step and
			# should be separated.
			ttest_results = stats.ttest_ind(experimental_values, control_values)
			signed_pvalue = ttest_results[1] if ttest_results[0] > 0 else ttest_results[1]*-1
			pvalues.append((symbol, signed_pvalue))

			gene_order.append(symbol)
			control.append(control_values)
			experimental.append(experimental_values)

	os.remove(full_path)
	return (pvalues, gene_order, control, experimental)