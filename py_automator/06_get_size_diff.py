import psycopg2
import os
from config import host, dbname, user, password, port, table_name, table
from config import host_k8s, dbname_k8s, user_k8s, password_k8s, port_k8s, table_name, table
from get_table_ddl import get_table_ddl
from exec_ddl import exec_ddl, ddl_table

def get_size_diff_rds():
    try:

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        cur = conn.cursor()
        print('Database connection of get_size_diff_rds is opened.')
        cur.execute("SELECT pg_catalog.pg_table_size(c.oid) as bytes FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam WHERE c.relkind IN ('r','p','v','m','S','f','') AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND n.nspname <> 'information_schema' and pg_catalog.pg_table_size(c.oid)/1024/1024 < 2000 AND pg_catalog.pg_table_is_visible(c.oid) AND c.relname = '%s'" % (table))
        table_size_rds = cur.fetchone()[0]

        # cur.execute("select (sum(pg_catalog.pg_table_size('%s')-pg_catalog.pg_table_size('%s'))/pg_catalog.pg_table_size('%s'))*100 as size_difference" % (table_name, ddl_table[1], table_name))
        # table_size_difference = cur.fetchone()[0]
        print('The size of %s table in bytes is: %s' % (table, table_size_rds))
        # print('The %s table is %s percent lighter than %s' % (ddl_table[1], table_size_difference, table_name))
        return table_size_rds

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_size_diff_rds is closed.') # Remove after tests

a = get_size_diff_rds()
print(a)
# print(a[0])
# print(table)
# print(ddl_table[0],ddl_table[1],ddl_table[2])

def get_size_diff_k8s():
    try:

        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s)

        cur = conn.cursor()
        print('Database connection of get_size_diff_k8s is opened.')
        cur.execute("set search_path to fdw,public,repack")
        cur.execute("SELECT pg_catalog.pg_table_size(c.oid) as bytes FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam WHERE c.relkind IN ('r','p','v','m','S','f','') AND n.nspname <> 'pg_catalog' AND n.nspname !~ '^pg_toast' AND n.nspname <> 'information_schema' and pg_catalog.pg_table_size(c.oid)/1024/1024 < 2000 AND pg_catalog.pg_table_is_visible(c.oid) AND c.relname = '%s'" % (ddl_table[2]))
        table_size = cur.fetchone()[0]

        print('The size of %s table in bytes is: %s' % (ddl_table[1], table_size))
        # print('The %s table is %s percent lighter than %s' % (ddl_table[1], table_size_difference, table_name))
        return table_size

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection of get_size_diff_k8s is closed.') # Remove after tests

b = get_size_diff_k8s()
print(b)
dif = (a-b)/a*100
print(dif)

# select (sum(pg_catalog.pg_table_size('%s')-pg_catalog.pg_table_size('%s'))/pg_catalog.pg_table_size('%s'))*100 as size_difference" % (table_name, ddl_table[1], table_name))