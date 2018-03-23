import sys

proj = sys.argv[2]
DRS_len = int(sys.argv[3]) 

for line in open(sys.argv[1]):

	
	

	parts = line.split('/')

	match = 0

	for i,pp in enumerate (parts):

		if pp == proj:
			match  = i
			break


	print '.'.join(parts[i:(i+DRS_len)])

