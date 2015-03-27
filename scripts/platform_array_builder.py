f = open('g2e/core/softfile/probe2gene.txt', 'r')

plats = {}
for line in f:
	p = line.split('\t')[0]
	plats[p] = True

l = [k for (k,v) in plats.items()]
print l

f.close()
