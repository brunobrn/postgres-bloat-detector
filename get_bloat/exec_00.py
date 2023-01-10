import psycopg2

from config import *
from subprocess import call
from table_bloat import get_tables

def exec_automation():
    TABLES_NAME = get_tables()
    if len(TABLES_NAME) >= 1:
        for exec in TABLES_NAME:
            call(["python", "get_bloat/exec_table_bloat.py", schema, exec[0]])
            # print(i[0])
    else:
        print('No tables to analyze')

exec_automation()