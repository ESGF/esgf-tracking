#!/bin/bash
PGPASSWORD=`cat /esg/config/.esg_pg_pass` psql -U dbsuper esgcet < $1