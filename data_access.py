import sys


def parse_url(url, proj, DRS_len):

	parts = line.split('/')
	match = 0

	for i,pp in enumerate (parts):

		if pp == proj:
			match  = i
			break

	return '.'.join(parts[i:(i+DRS_len)])


def parse_openid(x):

    parts = x.split('/')

    return parts[2], parts[5]



