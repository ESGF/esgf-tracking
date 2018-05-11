import random, sys

dset_list = []

for line in open(sys.argv[1]):

	dset_list.append(line.rstrip())


rnd = random.random
DCOUNT = len(dset_list)

dsarr = range(DCOUNT)

for i in range(DCOUNT):

	x = int(rnd()* DCOUNT )
	tmp = dsarr[i]
	dsarr[i] = dsarr[x]
	dsarr[x] = tmp

for i in dsarr:
	print dset_list[i]