import psycopg2
import os
from config import host_k8s, dbname_k8s, user_k8s, password_k8s, port_k8s, host, dbname,user,password,port

def create_fdw_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)
        cur = conn.cursor()
        print('Database connection of create_fdw_k8s is opened.')
        cur.execute("CREATE SERVER if not exists foreigndb_fdw FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '%s', port '%s', dbname '%s');" % (host, port, dbname))
        cur.execute("CREATE USER MAPPING if not exists FOR dba_pg_tools_username SERVER foreigndb_fdw OPTIONS (user '%s', password '%s');" % (user, password))
        cur.execute("GRANT USAGE ON FOREIGN SERVER foreigndb_fdw TO %s;" % (user))
        cur.execute("CREATE SCHEMA if not exists fdw;")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of create_fdw_k8s is closed.') 

create_fdw_k8s()
