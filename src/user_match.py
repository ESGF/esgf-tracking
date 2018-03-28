

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

	def match_record(pairs, dataset):

		for pair in pairs:

			if not pair["value"] == dataset[pair["key"]]:
				return False

		return True

	def match(comp_report):

		outdict = {}

		for comp_record in comp_report:

			for query_record in profile_records:		

				if match_record(query_record["pairs"], comp_record)


					for user in record["users"]:

						if not user in outdict:
							outdict["user"] = [comp_record]
						else:

							usrlst = outdict["user"]
							usrlst.append("comp_record")
							outdict["user"] = usrlst
		return outdict


