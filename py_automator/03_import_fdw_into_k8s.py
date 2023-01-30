import psycopg2
import os
from config import host_k8s, dbname_k8s, user_k8s, password_k8s, port_k8s, table_name_k8s, host, dbname,user,password,port,schema,table

def import_fdw_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)
        cur = conn.cursor()
        print('Database connection of import_fdw_k8s is opened.')
        cur.execute("DROP FOREIGN TABLE IF EXISTS fdw.%s" % (table))
        cur.execute("IMPORT FOREIGN SCHEMA  %s LIMIT TO (%s) FROM SERVER foreigndb_fdw INTO fdw;" % (schema, table))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of import_fdw_k8s is closed.') 

import_fdw_k8s()