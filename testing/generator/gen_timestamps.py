from datetime import datetime as dt


begin_datetimestamp = 48 * 365.25 * 24 * 3600

week = 60 * 60 * 24 * 7

NUM_PERIODS = 8
count = 4   # Per period

period = week / count

hp = period  / 2

tot_num = count * NUM_PERIODS

begin_off = begin_datetimestamp + hp

for i in range(tot_num):

	print dt.utcfromtimestamp(begin_off + (i * period)).isoformat()

