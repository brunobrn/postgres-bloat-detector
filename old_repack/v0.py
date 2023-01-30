import psycopg2
import os
from config import host, dbname, user, password, port, table_name, tuple_percent
from get_tuple_percent import get_tuple_percent
from execute_repack import execute_repack
from check_tuple import check_tuple

repack_result = execute_repack()
result = repack_result[0]

if result is True:
    check_tuple()
else:
    print("The repack isn't necessary")