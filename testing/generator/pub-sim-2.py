import random, json, os, sys
from time import time, sleep

from datetime import date, timedelta


PUB_INTERVAL = float(sys.argv[3])


DEBUG = False

TOT_PERIODS = int(sys.argv[2])

dset_list = []

dataset_paths = sys.argv[1]

for line in open(dataset_paths):

	dset_list.append(line)


rnd = random.random

DCOUNT = len(dset_list)

dsarr = range(DCOUNT)

p_count = 0

for i in range(DCOUNT):

	x = int(rnd()* DCOUNT )
	tmp = dsarr[i]
	dsarr[i] = dsarr[x]
	dsarr[x] = tmp

pub_list = []

PERIOD = 4  # Count per period

BASE = 2 * PERIOD # number of new-only events to complete
DRS_LEN = 10

quick_retract = -1


def exec_cmd(cmd):

# Dry run mode: print cmd
	os.system(cmd)

def update_dset(path):

	parts = path.split('/')

	version_str = parts[-1].rstrip()

	version_year = int(version_str[1:5])
	version_month = int(version_str[5:7])
	version_dom = int(version_str[7:9]) # day of month

	version_date = date(version_year, version_month, version_dom)
	td = timedelta(days=1)

	newverstr = (version_date + td).isoformat().replace('-','')

	prepath = '/'.join(path[0:-1])


	files = os.listdir(path)

	exec_cmd("mkdir " + prepath + 'files/d' + newverstr)
	exec_cmd("cd " + prepath + '; ln -s files/d' + newverstr + ' v' + newverstr)

	destpath = prepath + '/v' + newverstr

	for ff in files:

		newf = destpath + '/' + ff
		exec_cmd("cp " + path + '/' + ff + ' ' + newf)
		exec_cmd("echo -n '' >> " + newf)


	publish_path(destpath)
	return destpath

def publish_path(path):

	exec_cmd("esgmapfile --no-checksum --project cmip6test " + path)
	exec_cmd("esgpublish --project cmip6test --map mapfiles ")
	exec_cmd("esgpublish --project cmip6test --map mapfiles  --noscan --thredds")
	exec_cmd("esgpublish --project cmip6test --map mapfiles --noscan --publish")
	exec_cmd("rm -rf mapfiles")



def path_to_dset(path):

	parts = path.split('/')
	return '.'.join(path[3:-1]) + '#' + path[-1][1:]

def retract_dset(dset):

	exec_cmd("echo " + dset + " | esgunpublish --retract --project cmip6test --use-list -")


def main():

	print "running main"

	for i, idx in enumerate(dsarr): 

		if i == TOT_PERIODS:
			break

		starttime = time()

		if i < BASE:
			dset = dset_list[idx]
			print i, dset, "D-New-Dataset"
			publish_path(dset)
		else:
			if i % PERIOD <  (PERIOD -2):

				dset = dset_list[idx]
#				version = "v" + dset_list[idx][1]

	#			append_to_list(outlst, dset, version, ts)
				pub_list.append([dset, "PUB"])

				print i, dset, "D-New-Dataset"
				publish_path(dset)				



			elif i % PERIOD == (PERIOD - 2):
				# new version should be from old datasets - try this - could be retracted

				listlenbase = (len(pub_list) - 2)

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
							print "cat one", choice, len(pub_list) 
							print pub_list[choice]
					elif p_count == (TOT_PERIODS - 3):
						if DEBUG:
							print "find previous retraction"
						choice =quick_retract
						if DEBUG:
							print "cat two", choice, len(pub_list) 
							print pub_list[choice]
						dset_rec = pub_list[choice]
						break
					else:
						choice = int(rnd() * listlenbase)
						dset_rec = pub_list[choice]
						if dset_rec[1] == "PUB":
							break


	#			print "len:", listlenbase, "choice", choice

	

				print i, choice, dset, "E-New-version"
				newver  = update_dset(dset_rec[0])
				pub_list[choice] = [newver, "PUB" ] 

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
					
				dset_rec = pub_list[choice]

				# dset = dset_rec["master_id"]
				# outlst[choice]["retracted"] = True
				# outlst[choice]["latest"] = False

				# outlst[choice]["_timestamp"] = ts
				print i, choice, dset_rec, ret_str
				dset = dset_rec[0]
				retract_dset(path_to_dset(dset))
				pub_list[choice] = [dset, "RETR"]



		endtime = time()

		eltime = endtime - starttime

		sleep (PUB_INTERVAL - eltime )


	assert(p_count == TOT_PERIODS)


if __name__ == '__main__':
	main()
