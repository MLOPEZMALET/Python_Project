corpus = 'Neutre.txt'
corpus = open('Neutre.txt', 'r')
output = open('Neutre2.txt', 'w')
for line in corpus:
   line = line.replace(' ','\t')
   output.write(line)
