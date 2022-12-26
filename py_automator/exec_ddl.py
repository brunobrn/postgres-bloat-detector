import psycopg2
import os
from config import host, dbname, user, password, port, table_name
from get_table_ddl import get_table_ddl

ddl_table = get_table_ddl()

def exec_ddl():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()
        print('Database connection of exec_ddl is opened.')
        cur.execute(ddl_table[0])
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of exec_ddl is closed.') # Remove after tests

