import psycopg2
import os
from config import host_k8s, dbname_k8s, user_k8s, password_k8s, port_k8s, table_name_k8s, host, dbname,user,password,port,schema,table
from get_table_ddl import get_table_ddl

ddl_table = get_table_ddl()

def copy_table_to_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)
        cur = conn.cursor()
        print('Database connection of copy_table_to_k8s is opened.')

        cur.execute(ddl_table[0])

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of copy_table_to_k8s is closed.') 

copy_table_to_k8s()