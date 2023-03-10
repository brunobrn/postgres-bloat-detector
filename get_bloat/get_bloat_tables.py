import psycopg2
import sys

sys.path.insert(1, '/config') 

from config import *
from subprocess import call
from table_bloat import get_tables

def exec_automation():
    TABLES_NAME = get_tables()
    call(["python", "/migration/migration.py"])

    if len(TABLES_NAME) >= 1 and table == 'all':
        for tables in TABLES_NAME:       
            call(["python", "exec_table_bloat.py", schema, tables[0]])

    elif len(TABLES_NAME) >= 1 and table != 'all':
        call(["python", "exec_table_bloat.py", schema, table])

    else:
        print('No tables to analyze')

exec_automation()

