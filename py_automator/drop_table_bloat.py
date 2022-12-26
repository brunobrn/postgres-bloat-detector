import psycopg2
import os
from config import host, dbname, user, password, port, table_name
from get_table_ddl import get_table_ddl
from exec_ddl import exec_ddl, ddl_table

def drop_table_bloat():
    """ drop table bloat """
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        # create a cursor
        cur = conn.cursor()
        print('Database connection of drop_table_bloat is opened.')

        # Drop the table # this needs to be in another function and run in k8s in the future.
        cur.execute("drop table %s" % ddl_table[1])
        conn.commit()

        # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of drop_table_bloat is closed.') # Remove after tests
