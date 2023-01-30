import psycopg2
import os
from config import host_k8s, dbname_k8s, user_k8s, password_k8s, port_k8s, table_name_k8s

def create_type_oban_jobs():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)
        cur = conn.cursor()
        print('Database connection of create_type_oban_jobs is opened.')
        cur.execute("DROP TYPE IF EXISTS public.oban_job_state CASCADE")
        cur.execute("CREATE TYPE public.oban_job_state AS ENUM ('available', 'scheduled', 'executing', 'retryable', 'completed', 'discarded', 'cancelled')")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of create_type_oban_jobs is closed.') 

create_type_oban_jobs()