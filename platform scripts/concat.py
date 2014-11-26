import os
import pdb


PATH   = os.path.dirname(os.path.realpath(__file__)) + '/'
PARSED = PATH + 'parsed/'
CONCAT = PATH + 'concat/'


def concatenate():
	with open(PATH + 'probe2gene.py', 'w+') as out:

		# Create the dict.
		out.write('PROBE2GENE = {\n')
		out_str = ''

		for fn in os.listdir(PARSED):
			# Create a dict per platform.
			accession = fn.split('.')[0]

			out_str += '\t' + '"' + accession + '" : {' + '\n'
			
			# Output every mapping into its platform dict.
			# Build a string first so we can trim it down.
			plat_arr = []
			with open(PARSED + fn, 'r') as inp:
				next(inp)
				for line in inp:
					ln = line.split('\t')
					plat_arr.append('\t\t"' + str(ln[0]).strip() + '": "' + str(ln[1]).strip() + '"')

				# Add a newline to the very end of the string
				out_str += ',\n'.join(plat_arr) + '\n'
			out_str += '\t' + '},\n'

		# Remove newline and comma in order to remove the comma.
		# Re-add the newline.
		out_str = out_str[:-2] + '\n'
		out_str += '}'

		out.write(out_str)


if __name__ == '__main__':
	concatenate()