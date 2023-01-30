import psycopg2
import os
from config import host, dbname, user, password, port, table_name, tuple_percent
from get_tuple_percent import get_tuple_percent
from execute_repack import execute_repack

def check_tuple():
    """ Check the tuple percent after the repack*** """
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        # create a cursor
        cur = conn.cursor()
        cur.execute("select tuple_percent from pgstattuple('%s')" % table_name )
        tuple_after_repack = cur.fetchone()[0]
        print('Now the tuple_percent is: ', tuple_after_repack)
        print('The repack has been executed with sucess on database %s and table %s' % (dbname, table_name))

        # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed 3.') # Remove after tests
