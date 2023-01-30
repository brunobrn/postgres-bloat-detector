import psycopg2
from config import *

def get_tables():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()
        sql = '''SELECT c.relname as "Name"
                    FROM pg_catalog.pg_class c
                        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                        LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
                    WHERE c.relkind IN ('r','')
                        AND n.nspname <> 'pg_catalog'
                        AND n.nspname !~ '^pg_toast'
                        AND n.nspname <> 'information_schema'
                        AND n.nspname = 'public'
                        AND pg_catalog.pg_table_size(c.oid) < 200000
                    AND pg_catalog.pg_table_is_visible(c.oid)
                    ORDER BY 1;'''

        print('Database connection of get_tables is opened.')
        cur.execute("set search_path to pix,public,repack;")
        cur.execute(sql)
        table_names = cur.fetchall()

        return table_names

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_tables is closed.') # Remove after tests

table_name = get_tables()

for i in table_name:
    print(i[0])