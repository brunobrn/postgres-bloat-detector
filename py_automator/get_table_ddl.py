import psycopg2
import os
from config import host, dbname, user, password, port, table_name

def get_table_ddl():
    """ Get the creation command of table """
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        # create a cursor
        cur = conn.cursor()
        print('Database connection of get_table_ddl is opened.')
        cur.execute("select concat(create_table_1, tablespace_orig, create_table_2) from repack.tables where relname = '%s';" % table_name )
        ddl_table = cur.fetchone()[0]

        cur.execute("select (('repack.table_'::text || relid)) as table_name from repack.get_ddl_tables  where relname = '%s';" % table_name )
        oid_table = cur.fetchone()[0]

        cur.execute("select (('table_'::text || relid)) as temp_table_name from repack.get_ddl_tables  where relname = '%s';" % table_name )
        relname_table = cur.fetchone()[0]
        
        # close the communication with the PostgreSQL for this cursor
        cur.close()
        return ddl_table, oid_table, relname_table
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_table_ddl is closed.') # Remove after tests