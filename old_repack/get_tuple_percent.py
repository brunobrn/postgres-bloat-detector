import psycopg2
import os
from config import host, dbname, user, password, port, table_name, tuple_percent

def get_tuple_percent():
    """ Connect to the PostgreSQL database server to check tuple percent of oban_jobs"""
    
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
		# create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL check tuple percent of table %s on database %s' % (table_name, dbname))
        cur.execute("select tuple_percent from pgstattuple('%s')" % table_name )

        # display the PostgreSQL tuple percent
        tuple_percent = cur.fetchone()[0]
        print('The tuple_percent is: ',tuple_percent)
        return tuple_percent

	    # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed 1.') # Remove after tests