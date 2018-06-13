import sys, json
from user_match import DBSubscriptionMatcher
from datetime import datetime
from dateutil import parser as duparser
from dateutil import tz

from time import time

from esgf_feedback.send_job import process_users


SEND_EMAIL = False

VERBOSE = True  # enhanced print
begin_datetimestamp = 48 * 365.25 * 24 * 3600
#UPDATE_TYPE = "DAYS"
UPDATE_TYPE = "SECOND"
#UPDATE_PERIOD = 7 * 24 * 3600  # change to an argument
UPDATE_PERIOD = 20 * 60
UPDATE_PERIOD_DAYS = 7
INPUT_FILE = "subscriptions.json"

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
	res = compare_results(oldfn, newfn, case, intime)
	for it in res:
		print it["master_id"], it["update_status"]


SUBSFN = "/Users/ames4/git-repos/esgf-tracking/work/search-test/subs.json"

def subs_test(oldfn, newfn, case, intime):
	search_res = compare_results(oldfn, newfn, case, intime)
	matcher = DBSubscriptionMatcher()

	user_res = matcher.match(search_res)

	if SEND_EMAIL:
		process_users(user_res)
	else:
		print json.dumps(user_res, indent=1)



def compare_results(oldfn, newfn, case, intime):

	output_arr = []

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
		update_cond = False
		if UPDATE_TYPE == "DAYS":
			update_cond = (delta.days < UPDATE_PERIOD_DAYS)
		else:
			update_cond = (delta.seconds < UPDATE_PERIOD)
		if update_cond:
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
				if (not n["retracted"]) and n["latest"]:

					output_arr.append(n)
					output_arr[-1]["update_status"] = "new-retraction"
				elif VERBOSE:
					print outpre, master_id, "B-Old-Retratction"

		else:
			print outpre, "C-Quick-Retraction"

	for rec in updateornew:

		mstr = rec["master_id"]

		if not mstr in old_dict:
			output_arr.append(rec)
			output_arr[-1]["update_status"] = "new-dataset"

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
				output_arr.append(rec)
				output_arr[-1]["update_status"] = "new-version"

			else:
				print outpre,mstr, "G-Version-update-bug", newvers
	return output_arr

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
	subs_test(fn, infiles[idx], case, datetime.utcfromtimestamp(cur_ts) )	


