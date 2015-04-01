import os

outfile = open('probe2genes-append.txt', 'w+')

for filename in os.listdir(os.getcwd() + '/symbols'):
    if filename == '.DS_Store':
        continue

    with open('symbols/' + filename) as infile:
        for line in infile:
            outfile.write(line)
