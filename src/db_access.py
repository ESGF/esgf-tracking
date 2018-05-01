# for now a hardcoded dictionary
from sqlalchemy import create_engine
# from site_profile import get_prop_st
import os

PASS_FN = '/esg/config/.esg_pg_pass'

db_engine = None
has_db = False

def  init_db():
    
    if not os.path.exists(PASS_FN):
        return (False, None)
    
    f = open(PASS_FN)

    passwd = f.read().strip()
    
#    properties_obj = get_prop_st()

    # Defaults based on conventional node installation

    db_user = 'dbsuper'  # properties_obj.get('db.user', 'dbsuper')
    db_host = 'localhost' # properties_obj.get('db.host', 'localhost')
    db_port = '5432' # properties_obj.get('db.port', '5432')
    db_database = 'esgcet' # properties_obj.get('db.database', 'esgcet')
    db_str = ( 'postgresql://' + db_user +  ':' + passwd + '@' + db_host  +  ':' + db_port+ '/' + db_database)

    engine = create_engine(db_str)

    return True, engine


def get_table():


    if not has_db:
        return None

    qstr = "select * from esgf_subscriptions.subscribers"

    db_result = db_engine.execute(qstr)

    return db_result

