	for row in sortedColumns:
		total = 0
		for column, originalArrayIndex in enumerate(row):
			total += O2[originalArrayIndex, column]
		mean = total / len(row)
		for column, originalArrayIndex in enumerate(row):
			O2[originalArrayIndex, column] = mean

	print 'FIRST: ' + str(time.time() - start)