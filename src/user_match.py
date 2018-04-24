import json

from esgcet.exceptions import ESGMethodNotImplemented


from db_access import get_table

class BaseMatcher :

	def __init__(self, *args):
		raise  ESGMethodNotImplemented

	def match(self, *args):
		raise  ESGMethodNotImplemented



class SubscriptionMatcher(BaseMatcher):

	def __init__(self, inputfile):

		raise ESGMethodNotImplemented
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
		


class FileSubscriptionMatcher(SubscriptionMatcher):

	def __init__(self, inputfile):

		self.profile_records = json.load(open(inputfile))


class DBSubscriptionMatcher(SubscriptionMatcher):

	def format_kv(row):

		return {"key": row[1], "value": row[2] }



	def db_to_json():


		dbtable = get_table()

		tmp_dict = {}
		outjson = []

		for row in dbtable:

			key = row[0]
			if key in tmp_dict:
				tmpin = tmp_dict[key]
				tmpin.append(self.format_kv(row))
				tmp_dict[key] = tmpin	
			else:
				tmp_dict[key] = [self.format_kv(row)]
		for key in tmp_dict:
			outjson.append({ "pairs": tmp_dict[key] , "users": [key]})

		return outjson

	def __init__(self):
		self.profile_records = self.db_to_json()

