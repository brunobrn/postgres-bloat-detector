import os
import sys

# rds host
host=""
dbname="panda_notifications"
user="dbapy_database_username"
password="123456"
port=5432
python_arg=sys.argv[1:len(sys.argv)]
schema=python_arg[0]
table=python_arg[1]
tuple_percent=50
table_with_schema=schema+"."+table
table_name=schema+"."+table
# limit_size_table=python_arg[2] #mb


# k8s_bd_host
host_k8s=""
dbname_k8s="dbapy_database"
user_k8s="dbapy_database_username"
password_k8s="123456"
port_k8s=5432
table_name_k8s="public.oban_jobs"

# exec_py()

SET_SEARCH_PATH = ('''SET SEARCH_PATH TO %s;''' % (schema))

# create_fdw = __import__("02_create_fdw")
# import_fdw_into_k8s = __import__("03_import_fdw_into_k8s")

# from create_type_oban_01 import create_type_oban_jobs