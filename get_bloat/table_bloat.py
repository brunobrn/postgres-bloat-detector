import psycopg2
from config import *
from connections import *

# Create type oban_jobs_state to fix dependencie error.
def create_type_oban_jobs():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()

        # SQL Commands

        DDL_SCHEMA_K8S = ('''create schema if not exists %s''' % (schema))

        DDL_DROP_TYPE =  ('''DROP TYPE IF EXISTS %s.oban_job_state CASCADE''' % schema)

        DDL_CREATE_TYPE = ('''CREATE TYPE %s.oban_job_state AS ENUM 
                            ('available', 'scheduled', 'executing', 'retryable', 'completed', 'discarded', 'cancelled')
                            ''' % schema)

        # Execute Commands
        cur.execute(DDL_SCHEMA_K8S)
        cur.execute(DDL_DROP_TYPE)
        cur.execute(DDL_CREATE_TYPE)

        # Commit transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

create_type_oban_jobs()
# if table == 'oban_jobs':
#     create_type_oban_jobs()
# else:
#     pass

### ----------------------------------- ###

# Create FDW server on k8s host to copy and analyse data.
def create_fdw_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()
        
        # SQL Commands      
        DDL_CREATE_SERVER_FDW = ('''CREATE SERVER if not exists %s 
                                        FOREIGN DATA WRAPPER postgres_fdw 
                                            OPTIONS (host '%s', port '%s', dbname '%s');''' % (dbname, host, port, dbname))

        DDL_USER_MAPPING_FDW = ('''CREATE USER MAPPING if not exists FOR dba_pg_tools_username 
                                    SERVER %s 
                                        OPTIONS (user '%s', password '%s');''' % (dbname, user, password))

        DDL_GRANT_FDW = ('''GRANT USAGE ON FOREIGN SERVER %s TO %s;''' % (dbname, user))

        DDL_CREATE_SCHEMA_DBA = ('''CREATE SCHEMA if not exists dba;''')

        DDL_CREATE_SCHEMA_FDW = ('''CREATE SCHEMA if not exists fdw;''')

        # Execute Commands
       
        cur.execute(DDL_CREATE_SERVER_FDW)
        cur.execute(DDL_USER_MAPPING_FDW)
        cur.execute(DDL_GRANT_FDW)
        cur.execute(DDL_CREATE_SCHEMA_DBA)
        cur.execute(DDL_CREATE_SCHEMA_FDW)

        # Commit transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### ----------------------------------- ###

# Import FDW table in k8s schema.
def import_fdw_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()

        # SQL Commands
        DROP_FOREIGN_TABLE = ('''DROP FOREIGN TABLE IF EXISTS fdw.%s''' % (table))

        IMPORT_FOREIGN_TABLE = ('''IMPORT FOREIGN SCHEMA  %s LIMIT TO (%s) 
                                    FROM SERVER %s INTO fdw;''' % (schema, table, dbname))

        # Execute Commands
        cur.execute(DROP_FOREIGN_TABLE)
        cur.execute(IMPORT_FOREIGN_TABLE)

        # Commit transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


### ----------------------------------- ###

# Get the table DDL commands to create table in k8s exactly like main database
def get_table_ddl():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, application_name=app_name)
        cur = conn.cursor()
        cur.execute(SET_SEARCH_PATH)

        # SQL Commands
        GET_DDL_TABLE = ('''select concat(create_table_1, tablespace_orig, create_table_2) 
                                from dba.get_ddl_tables where relname = '%s';''' % table_name )

        GET_OID_TABLE = ('''select (('dba.table_'::text || relid)) as table_name 
                                from dba.get_ddl_tables  where relname = '%s';''' % table_name )

        GET_RELNAME_TABLE = ('''select (('table_'::text || relid)) as temp_table_name 
                                from dba.get_ddl_tables  where relname = '%s';''' % table_name )

        # Execute Commands
        cur.execute(GET_DDL_TABLE)
        ddl_table = cur.fetchone()[0]

        cur.execute(GET_OID_TABLE)
        oid_table = cur.fetchone()[0]

        cur.execute(GET_RELNAME_TABLE)
        relname_table = cur.fetchone()[0]

        # End transactions
        cur.close()
        return ddl_table, oid_table, relname_table

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Exec get_table_ddl function
DDL_TABLE = get_table_ddl()

### ----------------------------------- ###

# Exec the copy to create table in k8s with the same data of main database
def copy_table_to_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()

        # SQL Commands
        DROP_TABLE_K8S = ('''DROP TABLE IF EXISTS %s''' % DDL_TABLE[1])

        # Execute Commands
        cur.execute(DROP_TABLE_K8S)
        cur.execute(DDL_TABLE[0])

        # End transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### ----------------------------------- ###

# Get the size of main database table
def get_size_diff_rds():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, application_name=app_name)
        cur = conn.cursor()
        cur.execute(SET_SEARCH_PATH)
        
        # SQL Commands
        SIZE_MAIN_TABLE = ('''SELECT PG_CATALOG.PG_TABLE_SIZE(C.OID) AS BYTES
                    FROM PG_CATALOG.PG_CLASS C
                    LEFT JOIN PG_CATALOG.PG_NAMESPACE N ON N.OID = C.RELNAMESPACE
                    LEFT JOIN PG_CATALOG.PG_AM AM ON AM.OID = C.RELAM
                    WHERE C.RELKIND IN ('r','p','v','m','S','f','')
                        AND N.NSPNAME <> 'pg_catalog'
                        AND N.NSPNAME !~ '^pg_toast'
                        AND N.NSPNAME <> 'information_schema'
                        AND PG_CATALOG.PG_TABLE_IS_VISIBLE(C.OID)
	                    AND C.RELNAME = '%s' ''' % (table))

        # Execute Commands
        cur.execute(SIZE_MAIN_TABLE)
        MAIN_TABLE_SIZE = cur.fetchone()[0]
        print('The size of %s table in bytes is: %s' % (table, MAIN_TABLE_SIZE))

        # End transactions    
        cur.close()    
        return MAIN_TABLE_SIZE

    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
### ----------------------------------- ###

# Get the size of k8s database table
def get_size_diff_k8s():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()
        
        # SQL Commands
        SET_SEARCH_PATH_K8S = ('''set search_path to fdw,dba,public,%s''' % (schema))

        SIZE_K8S_TABLE = ('''SELECT pg_catalog.pg_table_size(c.oid) as bytes 
                                FROM pg_catalog.pg_class c 
                                    LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
                                    LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
                                WHERE c.relkind IN ('r','p','v','m','S','f','') 
                                    AND n.nspname <> 'pg_catalog' 
                                    AND n.nspname !~ '^pg_toast' 
                                    AND n.nspname <> 'information_schema' 
                                    AND pg_catalog.pg_table_is_visible(c.oid) 
                                    AND c.relname = '%s' ''' % (DDL_TABLE[2]))

        # Execute Commands
        cur.execute(SET_SEARCH_PATH_K8S)
        cur.execute(SIZE_K8S_TABLE)
        K8S_TABLE_SIZE = cur.fetchone()[0]
        print('The size of %s table in bytes is: %s' % (DDL_TABLE[1], K8S_TABLE_SIZE))

        # End transactions     
        cur.close()
        return K8S_TABLE_SIZE

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        
### ----------------------------------- ###

# Drop tables on k8s size to save storage
def drop_table_bloat():
    try:
        conn = psycopg2.connect(dbname=dbname_k8s, user=user_k8s, password=password_k8s, host=host_k8s, port=port_k8s, application_name=app_name)
        cur = conn.cursor()

        # SQL Commands
        DROP_TABLE_K8S = ('''DROP TABLE IF EXISTS %s''' % DDL_TABLE[1])
        DROP_FOREIGN_TABLE = ('''DROP FOREIGN TABLE IF EXISTS fdw.%s;''' % (table))

        # Execute Commands
        cur.execute(DROP_TABLE_K8S)
        cur.execute(DROP_FOREIGN_TABLE)

        # End transactions     
        conn.commit()
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


### ----------------------------------- ###

# Get the name of tables in the schema
def get_tables():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, application_name=app_name)
        cur = conn.cursor()
        cur.execute(SET_SEARCH_PATH)

        # SQL commands   
        GET_TABLES = ('''SELECT c.relname as "Name"
                    FROM pg_catalog.pg_class c
                        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                        LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
                    WHERE c.relkind IN ('r','')
                        AND n.nspname <> 'pg_catalog'
                        AND n.nspname !~ '^pg_toast'
                        AND n.nspname <> 'information_schema'
                        AND c.relpersistence = 'p'
                        AND pg_catalog.pg_table_size(c.oid)/1024/1024 > 0
                        AND pg_catalog.pg_table_size(c.oid)/1024/1024 < 500
                        AND c.relname not like '%_p%_w%'
                    AND pg_catalog.pg_table_is_visible(c.oid)
                    ORDER BY 1;''') 
      
        # Execute commands
        cur.execute(GET_TABLES)
        TABLES_NAME = cur.fetchall()
        
        # End transacations
        cur.close()
        return TABLES_NAME

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### ----------------------------------- ###

# Get the name of schema inn the database
def get_schemas():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port, application_name=app_name)
        cur = conn.cursor()
        cur.execute(SET_SEARCH_PATH)

        # SQL commands   
        GET_SCHEMAS = ('''SELECT n.nspname AS "Name"
                            FROM pg_catalog.pg_namespace n
                                WHERE n.nspname !~ '^pg_' 
                            AND n.nspname not in ('information_schema','dba','cron','partman','pghero','repack','monitoring');''') 
      
        # Execute commands
        cur.execute(GET_SCHEMAS)
        SCHEMAS_NAME = cur.fetchall()
        
        # End transacations
        cur.close()
        return SCHEMAS_NAME

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()