import psycopg2
import os
from connections import *

def exec_sleep():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)
        cur = conn.cursor()
        print('Database connection of sleep is opened.')
        cur.execute("select pg_sleep(5000)")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of sleep is closed.') # Remove after tests


exec_sleep()