import psycopg2
import os
from config import host, dbname, user, password, port, table_name


def get_table_size():
    """ Get table size """
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        # create a cursor
        cur = conn.cursor()
        cur.execute("SELECT pg_catalog.pg_table_size(c.oid)/1024/1024 as MB FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam WHERE c.relkind IN ('r','p','v','m','S','f','') AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND n.nspname <> 'information_schema' and pg_catalog.pg_table_size(c.oid)/1024/1024 < 2000 AND pg_catalog.pg_table_is_visible(c.oid) AND c.relname = '%s';" % table_name )
        table_size = cur.fetchone()[0]
        print('The size of %s table in MB is: %s' % (table_name, table_size))
        print('printa essa linha %s and table %s' % (dbname, table_name))

        # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_table_size is closed.') # Remove after tests

get_table_size()