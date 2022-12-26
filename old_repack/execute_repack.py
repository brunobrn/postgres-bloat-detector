import psycopg2
import os
from config import host, dbname, user, password, port, table_name, tuple_percent
from get_tuple_percent import get_tuple_percent

def execute_repack():
    """ If the table tuple_percent is less than tuple_percent env, then execute repack on it """
    
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
		
        # create a cursor
        cur = conn.cursor()

        if get_tuple_percent() < tuple_percent:            
            os.system('echo "%s:5432:%s:%s:%s" >> ~/.pgpass' % (host, dbname, user, password))
            os.system('chmod 0600 ~/.pgpass')
            os.system('pg_repack -h %s -p 5432 -U %s -t %s -D -T 500 -k %s' % (host, user, table_name, dbname))
            return True, print('Repack executed with success')
            
        else: return False, print('The tuple percent of %s is bigger than %s'% (table_name, tuple_percent))

        # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed 2.') # Remove after tests
