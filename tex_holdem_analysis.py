import csv

with open('texasholdem_output.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    data = [row for row in reader]


types = list(set([d[-1] for d in data[1:]])); types.sort()
type_counts = [d[-1] for d in data[1:]]

for t in types:
    print(t, type_counts.count(t), type_counts.count(t)/len(type_counts))



