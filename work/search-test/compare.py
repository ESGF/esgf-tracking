import sys, json

#old = json.load(open(sys.argv[1]))

#new = json.load(open(sys.argv[2]))

VERBOSE = False  # enhanced print


begin_datetimestamp = 48 * 365.25 * 24 * 3600

UPDATE_PERIOD = 7 * 24 * 3600  # change to an argument

#UPDATE_PERIOD = 20 * 60

UPDATE_PERIOD_DAYS = 7
#UPDATE_PERIOD_MIN = 7 * 24 * 60

from datetime import datetime

from dateutil import parser as duparser
from dateutil import tz


# UPDATE_PERIOD = 17 # days ; so must be at least one

def convert(ts):

	return duparser.parse(ts)
	# convert timestamp to datetime


def get_latest(obj):

	oldts = convert(obj["response"]["docs"][0]["_timestamp"])

	for it in obj["response"]["docs"][1:]:

		ts = convert(it["_timestamp"])

		# if ts is newer than old ts
		if ts > oldts:
			oldts = ts

	return oldts


def convert_test(oldfn, newfn, case, intime):

	outpre = str(case) + " " + oldfn + " " + newfn
	retract_lst = []
	updateornew = []
	old_dict = {}

	old = json.load(open(oldfn))
	new = json.load(open(newfn))

	for rec in old["response"]["docs"]:

		mid = rec["master_id"]
		if mid in old_dict:
			arr = old_dict[mid]
			arr.append(rec)
			old_dict[mid] = arr	
		else:
			old_dict[mid] = [rec]

	for rec in new["response"]["docs"]:

		dset_time = convert(rec["_timestamp"])

		delta = intime - dset_time 

#		print "delta days", delta.days
		if delta.days < UPDATE_PERIOD_DAYS:
			if rec["retracted"]:
#				print "found retracted in UPDATE_PERIOD", rec["master_id"]
				retract_lst.append(rec)
			else:
				updateornew.append(rec)
		elif rec["retracted"]:
#			print "found retracted OLD NEWS", rec["master_id"]
			retract_lst.append(rec)
#		else:
#			print rec, "Nothing"

	for rec in retract_lst:

		master_id = rec["master_id"]

		if master_id in old_dict:
			lookup = old_dict[master_id]


#			print len(lookup), "datasets in retratcted set"
			for n in lookup:
#				print  n 
				if not n["retracted"]:

					print outpre, master_id, "A-New-Retratction"
				elif VERBOSE:
					print outpre, master_id, "B-Old-Retratction"

		else:
			print outpre, "C-Quick-Retraction"

	for rec in updateornew:

		mstr = rec["master_id"]

		if not mstr in old_dict:
			print outpre, mstr, "D-New-Dataset"
		else:
			newvers = rec["version"]
			lookup = old_dict[rec["master_id"]]
			newpub = True

			oldids = []

			for oldrec in lookup:
				oldvers = oldrec["version"]
#				print oldvers, newvers
				if  oldvers >= newvers:
					print outpre,mstr, "F-Not-new-version", newvers,  oldvers
				else:
					oldids.append(oldvers)
			
			if len(oldids) > 0:
				print outpre,mstr, "E-New-version", newvers,  ','.join(oldids)
			else:
				print outpre,mstr, "G-Version-update-bug", newvers

if len(sys.argv) < 4:
	print "Usage:"
	print "   python compare.py <base-index>  <filename1> <filename2> ..."
	print "minimum two files required"
	exit(-1)

advance = int(sys.argv[1])

infiles = sys.argv[2:]


cur_ts = begin_datetimestamp + (UPDATE_PERIOD  * (1 + advance))

for case, fn in enumerate(infiles[0:-1]):


	print
	print "BEGIN ROUND", case
	print

	cur_ts += UPDATE_PERIOD
	idx = case +1

#	print "Time of query: " , cur_ts

	convert_test(fn, infiles[idx], case, datetime.utcfromtimestamp(cur_ts) )	


