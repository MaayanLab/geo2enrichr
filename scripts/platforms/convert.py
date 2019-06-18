import os
import csv


LOG = 'log_symbols.txt'


human_canonical_symbols = set()
with open('gene_synonyms/genesym_geneid_human_20140825.txt', 'r') as tsv:
    for line in csv.reader(tsv, delimiter='\t'):
        human_canonical_symbols.add(line[0])

human_synonyms = {}
with open('gene_synonyms/genesym_geneid_synonym_human_20140825.txt', 'r') as tsv:
    for line in csv.reader(tsv, delimiter='\t'):
        human_synonyms[line[2]] = line[0]

mouse_canonical_symbols = set()
with open('gene_synonyms/genesym_geneid_mouse_20140825.txt', 'r') as tsv:
    for line in csv.reader(tsv, delimiter='\t'):
        mouse_canonical_symbols.add(line[0])

mouse_synonyms = {}
with open('gene_synonyms/genesym_geneid_synonym_mouse_20140825.txt', 'r') as tsv:
    for line in csv.reader(tsv, delimiter='\t'):
        mouse_synonyms[line[2]] = line[0]

mouse_2_humans = {}
with open('gene_synonyms/humangenesym_humangeneid_mousegenesym_mousegeneid_20140825.txt', 'r') as tsv:
    for line in csv.reader(tsv, delimiter='\t'):
        mouse_2_humans[line[0]] = line[2]


def handle_symbols(filename):
    accession = filename.split('.')[0]
    num_lines = 0
    num_converted = 0

    with open('cleaned/' + filename, 'r') as tsv, open('symbols/' + filename, 'w+') as out:

        write = lambda x, y: out.write(accession + '\t' + x + '\t' + y + '\n')

        for line in csv.reader(tsv, delimiter='\t'):
            num_lines += 1
            probe_id = line[1]
            gene_symbol = line[2]

            # HUMANS
            # Is the symbol a canonical human symbol?
            if gene_symbol in human_canonical_symbols:
                write(probe_id, gene_symbol)
                num_converted += 1
                continue

            # Is it a human synonym? Then use the canonical value
            if gene_symbol in human_synonyms:
                canon_sym = human_synonyms[gene_symbol]
                if not canon_sym in human_canonical_symbols:
                    raise Exception('Canonical gene symbol not in list')
                write(probe_id, canon_sym)
                num_converted += 1
                continue

            # MICE
            # Is the symbol a canonical mouse symbol? Convert it to human if possible.
            if gene_symbol in mouse_canonical_symbols:
                if gene_symbol in mouse_2_humans:
                    write(probe_id, mouse_2_humans[gene_symbol])
                    num_converted += 1
                    continue
            
            if gene_symbol in mouse_synonyms:
                if gene_symbol in mouse_2_humans:
                    write(probe_id, mouse_2_humans[gene_symbol])
                    num_converted += 1
                    continue
    
    if num_converted < 5000:
        with open(LOG, 'a') as log:
            log.write(accession + '\n')
            log.write('lines: ' + str(num_lines) + '\n')
            log.write('converted: ' + str(num_converted) + '\n')
            log.write('\n')
        os.remove('symbols/' + filename)
    else:
    	print('Converted ' + accession)


if __name__ == '__main__':
    f = open(LOG, 'w+')
    f.close()
    for filename in os.listdir(os.getcwd() + '/downloaded'):
        handle_symbols(filename)
