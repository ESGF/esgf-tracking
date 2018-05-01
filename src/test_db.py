from db_access import ESG_DB_Access

db = ESG_DB_Access()

res = db.get_table()

if res is None:
    exit(-1)

