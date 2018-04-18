import json

from esgcet.exceptions import ESGMethodNotImplemented


class BaseMatcher :

	def __init__(self, *args):
		raise  ESGMethodNotImplemented

	def match(self, *args):
		raise  ESGMethodNotImplemented



class FileSubscriptionMatcher(BaseMatcher):

	def __init__(self, inputfile):

		self.profile_records = json.load(open(inputfile))
		# get config

	def extract_fields(self, rec):

		return { "master_id" : rec["master_id"] , "update_status" : rec["update_status"]}

	def match_record(self, pairs, dataset):

		for pair in pairs:

			if not dataset[pair["key"]] in pair["value"]:
				return False

		return True

	def match(self, comp_report):

		self.outdict = {}

		for comp_record in comp_report:

			for query_record in self.profile_records:		

				if self.match_record(query_record["pairs"], comp_record):

					for user in query_record["users"]:

						if not user in outdict:
							outdict[user] = [self.extract_fields(comp_record)]
						else:

							usrlst = outdict[user]
							usrlst.append(self.extract_fields(comp_record))
							outdict[user] = usrlst
		


