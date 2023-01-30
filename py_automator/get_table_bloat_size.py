import psycopg2
import os
from config import host, dbname, user, password, port, table_name
from get_table_ddl import get_table_ddl
from exec_ddl import exec_ddl, ddl_table

def get_table_bloat_size():
    """ Get table bloat size """
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        # create a cursor
        cur = conn.cursor()
        print('Database connection of get_table_bloat_size is opened.')
        cur.execute("SELECT pg_catalog.pg_table_size(c.oid)/1024/1024 as MB FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam WHERE c.relkind IN ('r','p','v','m','S','f','') AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND n.nspname <> 'information_schema' and pg_catalog.pg_table_size(c.oid)/1024/1024 < 2000 AND pg_catalog.pg_table_is_visible(c.oid) AND c.relname = '%s'" % (ddl_table[2]))
        table_size = cur.fetchone()[0]

        # get the size difference between the two tables
        cur.execute("select (sum(pg_catalog.pg_table_size('%s')-pg_catalog.pg_table_size('%s'))/pg_catalog.pg_table_size('%s'))*100 as size_difference" % (table_name, ddl_table[1], table_name))
        table_size_difference = cur.fetchone()[0]
        print('The size of %s table in MB is: %s' % (ddl_table[1], table_size))
        print('The %s table is %s percent lighter than %s' % (ddl_table[1], table_size_difference, table_name))

        # close the communication with the PostgreSQL for this cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_table_bloat_size is closed.') # Remove after tests
