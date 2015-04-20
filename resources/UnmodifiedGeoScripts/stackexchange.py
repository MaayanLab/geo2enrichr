"""
Quantile normalization

License: 
Creative Commons Attribution-ShareAlike 3.0 Unported License
http://creativecommons.org/licenses/by-sa/3.0/

This is an implementation of quantile normalization for microarray data analysis.
CSV files must not contain header. Format must be as follows:
    | Gene | Expression value |
Example:
    | ABCD1 | 5.675 |

Other restrictions:
1.) Each csv file must contain the same gene set. 
2.) Each gene must be unique.

Usage on command line:
    python2.7 quantile_normalization *csv
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import sys


if (len(sys.argv) > 1):
    file_list = sys.argv[1:]
else:
    print "Not enough arguments given."
    sys.exit()

# Parse csv files for samples, creating lists of gene names and expression values.
set_dict = {}
for path in file_list:
    with open(path) as stream:
        data = list(csv.reader(stream, delimiter = '\t'))
    data = sorted([(i, float(j)) for i, j in data], key = lambda v: v[1])
    sample_genes = [i for i, j in data]
    sample_values = [j for i, j in data]
    set_dict[path] = (sample_genes, sample_values)

# Create sorted list of genes and values for all datasets.
set_list = [x for x in set_dict.items()]
set_list.sort(key = lambda (x,y): file_list.index(x))
    
# Compute row means.
L = len(file_list)
all_sets = [[i] for i in set_list[0:L+1]]
sample_values_list = [[v for i, (j, k) in A for v in k] for A in all_sets]
mean_values = [sum(p) / L for p in zip(*sample_values_list)]

# Compute histogram bin size using Rice Rule
for sample in sample_values_list:
    bin_size = int(pow(2 * len(sample), 1.0 / 3.0))

# Provide corresponding gene names for mean values and replace original data values by corresponding means.
sample_genes_list = [[v for i, (j, k) in A for v in j] for A in all_sets]
sample_final_list = [sorted(zip(sg, mean_values)) for sg in sample_genes_list]

# Compute normalized histogram bin size using Rice Rule
for sample in sample_final_list:
    bin_size_2 = int(pow(2 * len(sample), 1.0 / 3.0))

# Creates a dictionary with normalized values for the dataset.
def exp_pull(sample, gene):
    sample_name = {genes: values for genes, values in 
                    zip([v for i, (j, k) in set_list[sample - 1:sample] 
                    for v in j], mean_values)}
    return round(sample_name.get(gene, 0), 3)

# Truncate full path name to yield filename only.
file_list = [file[file.rfind("/") + 1:file.rfind(".csv")] for file in file_list]

# Pulls normalized expression values for particular genes for all samples.
genes_of_interest = ['ERG', 'ETV1', 'ETV4', 'ETV5']
    
for gene in genes_of_interest:
    print '\n{}:'.format(gene)
    for i, file in enumerate(file_list, 1):
        print '{}: {}'.format(file, exp_pull(i, gene))

# Plot an overlayed histogram of raw data.
fig = plt.figure(figsize=(12,12))
ax1 = fig.add_subplot(221)

sample_graph_list_raw = [[i for i in sample_value] for sample_value in sample_values_list]
    
colors = ['b', 'g', 'r', 'c', 'm', 'y']
color_list = [random.choice(colors) for file in file_list]

for graph, color, file in zip(sample_graph_list_raw, color_list, file_list):
    plt.hist(graph, bins = bin_size, histtype = 'stepfilled', normed = True, color = None, 
                alpha = 0.5, label = file) 
    
plt.title("Microarray Expression Frequencies")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()

# Plot an overlayed histogram of normalized data.
ax2 = fig.add_subplot(222)
sample_graph_list = [[j for i, j in sample_final] for sample_final in sample_final_list]

for graph, color, file in zip(sample_graph_list, color_list, file_list):
    plt.hist(graph, bins = bin_size_2, histtype = 'stepfilled',
             normed = True, color = color, alpha = 0.5 , label = file)   
                      
plt.title("Microarray Expression Frequencies (normalized)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()

# Plot box plots of raw data.
ax3 = fig.add_subplot(223)
plt.title("Microarray Expression Values")
plt.hold = True
boxes = [graph for graph in sample_graph_list_raw]
plt.boxplot(boxes, vert = 1)

# Plot box plots of normalized data.
ax4 = fig.add_subplot(220)
plt.title("Microarray Expression Values (normalized)")
plt.hold = True
boxes = [graph for graph in sample_graph_list]
plt.boxplot(boxes, vert = 1)

plt.savefig('figures.pdf')
plt.savefig('figures.png')
plt.show()