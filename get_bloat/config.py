import sys

python_arg=sys.argv[1:len(sys.argv)]
schema=python_arg[0]
table=python_arg[1]
table_with_schema=schema+"."+table
table_name=schema+"."+table
SET_SEARCH_PATH = ('''SET SEARCH_PATH TO %s;''' % (schema))
# limit_size_table=python_arg[2] #mb
