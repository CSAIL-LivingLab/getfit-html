dates = []
for res in resultArray:
    for t in res.tuples:
        dates.append(t.cells[0])

slicedDates = []
for date in dates:
    slicedDates.append(date[0:10])

sorted(slicedDates, key=lambda d: map(int, d.split('-')))