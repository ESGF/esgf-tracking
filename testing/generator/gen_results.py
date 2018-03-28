import random, json

def write_out(lst, step):

	out = { 'response': {'docs' : lst} }

	outf = open("results." + str(step) + ".json", "w")

	outf.write(json.dumps(out, sort_keys=True, indent=4, separators=(',', ': ')))
	outf.close()

dataset_ids = "dset_id.lst"
timestamps = "ts.txt"

DEBUG = False

TOT_PERIODS = 8

dset_list = []

for line in open(dataset_ids):

	dset_list.append(line.rstrip().split('#'))


rnd = random.random

DCOUNT = len(dset_list)

dsarr = range(DCOUNT)

p_count = 0

for i in range(DCOUNT):

	x = int(rnd()* DCOUNT )
	tmp = dsarr[i]
	dsarr[i] = dsarr[x]
	dsarr[x] = tmp

outlst = []

PERIOD = 4  # Count per period

BASE = 2 * PERIOD # number of new-only events to complete



nv_choice = -1

def append_to_list(outlist, dset, version, ts):
	record = {}
	record["master_id"] = dset
	record["version"] = version
	record["retracted"] = False
	record["_timestamp"] = ts
	record["latest"] = True
	outlist.append(record)

quick_retract = -1

for i, ts in  enumerate(open(timestamps)):

	if i < BASE:
		idx = dsarr.pop()
		dset = dset_list[idx][0]
		version = "v" + dset_list[idx][1]

		append_to_list(outlst, dset, version, ts)
		print i, dset, "D-New-Dataset"
	else:
		if i % PERIOD <  (PERIOD -2):
			idx = dsarr.pop()
			dset = dset_list[idx][0]
			version = "v" + dset_list[idx][1]
			append_to_list(outlst, dset, version, ts)
			print i, len(outlst) - 1, dset, "D-New-Dataset"

		elif i % PERIOD == (PERIOD - 2):
			# new version should be from old datasets - try this - could be retracted

			listlenbase = (len(outlst) - 2)

			dset_rec = None
			choice = -1
			# additional case update a retracted version
			# quick new version

			while True:

				if p_count == (TOT_PERIODS - 2):

					if DEBUG:
						print "find quick new version"
					choice = ((TOT_PERIODS - 3) * PERIOD)
					if DEBUG:
						print "cat one", choice, len(outlst) 
						print outlst[choice]
				elif p_count == (TOT_PERIODS - 3):
					if DEBUG:
						print "find previous retraction"
					choice =quick_retract
					if DEBUG:
						print "cat two", choice, len(outlst) 
						print outlst[choice]
					dset_rec = outlst[choice]
					break
				else:
					choice = int(rnd() * listlenbase)
				dset_rec = outlst[choice]

				if dset_rec["latest"]:
					break

#			print "len:", listlenbase, "choice", choice

			dset = dset_rec["master_id"]
			oldversion = dset_rec["version"]
			numversion = int(oldversion[1:])
			version = "v" + str(numversion + 1)
			outlst[choice]["latest"] = False
			append_to_list(outlst, dset, version, ts)			
			print i, choice, dset, "E-New-version", oldversion, version

		else:
			assert(i % PERIOD == PERIOD -1)


			choice = -1
			while True:

				if p_count == (TOT_PERIODS - 1):
					# quick retraction
					choice = ((TOT_PERIODS - 2) * PERIOD)
					if DEBUG:
						print choice, len(outlst), "C-Quick-Retraction"
					ret_str = "C-Quick-Retraction"
				else:
					choice = int(rnd() * (len(outlst) -3))
					ret_str = "A-New-Retraction"
					quick_retract= choice

				dset_rec = outlst[choice]
				if (not dset_rec["retracted"]) and dset_rec["latest"]:
					break

			dset = dset_rec["master_id"]
			outlst[choice]["retracted"] = True
			outlst[choice]["latest"] = False

			outlst[choice]["_timestamp"] = ts
			print i, choice, dset, ret_str

	if i % PERIOD == PERIOD -1:

		write_out(outlst, i / PERIOD)
		p_count = p_count + 1

assert(p_count == TOT_PERIODS)

