file = open('covid2.aminseq',mode='r')
genome = file.read()
genome = genome.replace("\n", "")
# https://www.ncbi.nlm.nih.gov/nuccore/306569684
# says spike is from 22906 to 26976
# since python starts from 0
print(genome[22907:26976])

file.close()