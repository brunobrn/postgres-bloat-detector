import sys

sys.path.insert(1, '/config') 

from config import *
from connections import *

SET_SEARCH_PATH=('''SET SEARCH_PATH TO %s;''' % (schema))

SET_SEARCH_PATH_K8S = ('''set search_path to fdw,dba,public,%s''' % (schema))

DDL_SCHEMA_K8S = ('''create schema if not exists %s''' % (schema))

DDL_DROP_TYPE =  ('''DROP TYPE IF EXISTS %s.oban_job_state CASCADE''' % schema)

DDL_CREATE_TYPE = ('''CREATE TYPE %s.oban_job_state AS ENUM 
                            ('available', 'scheduled', 'executing', 'retryable', 'completed', 'discarded', 'cancelled')
                            ''' % schema)

DDL_CREATE_SERVER_FDW = ('''CREATE SERVER if not exists %s 
                                FOREIGN DATA WRAPPER postgres_fdw 
                                    OPTIONS (host '%s', port '%s', dbname '%s');''' % (dbname, host, port, dbname))

DDL_USER_MAPPING_FDW = ('''CREATE USER MAPPING if not exists FOR dba_pg_tools_username 
                            SERVER %s 
                                OPTIONS (user '%s', password '%s');''' % (dbname, user, password))

DDL_GRANT_FDW = ('''GRANT USAGE ON FOREIGN SERVER %s TO %s;''' % (dbname, user))

DDL_CREATE_SCHEMA_DBA = ('''CREATE SCHEMA if not exists dba;''')

DDL_CREATE_SCHEMA_FDW = ('''CREATE SCHEMA if not exists fdw;''')

DROP_FOREIGN_TABLE = ('''DROP FOREIGN TABLE IF EXISTS fdw.%s''' % (table))

IMPORT_FOREIGN_TABLE = ('''IMPORT FOREIGN SCHEMA  %s LIMIT TO (%s) 
                            FROM SERVER %s INTO fdw;''' % (schema, table, dbname))

GET_DDL_TABLE = ('''select concat(create_table_1, tablespace_orig, create_table_2) 
                        from dba.get_ddl_tables where relname = '%s';''' % table_name )

GET_OID_TABLE = ('''select (('dba.table_'::text || relid)) as table_name 
                        from dba.get_ddl_tables  where relname = '%s';''' % table_name )

GET_RELNAME_TABLE = ('''select (('table_'::text || relid)) as temp_table_name 
                        from dba.get_ddl_tables  where relname = '%s';''' % table_name )

# DROP_TABLE_K8S = ('''DROP TABLE IF EXISTS %s''' % DDL_TABLE[1])

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

# SIZE_K8S_TABLE = ('''SELECT pg_catalog.pg_table_size(c.oid) as bytes 
#                                 FROM pg_catalog.pg_class c 
#                                     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
#                                     LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
#                                 WHERE c.relkind IN ('r','p','v','m','S','f','') 
#                                     AND n.nspname <> 'pg_catalog' 
#                                     AND n.nspname !~ '^pg_toast' 
#                                     AND n.nspname <> 'information_schema' 
#                                     AND pg_catalog.pg_table_is_visible(c.oid) 
#                                     AND c.relname = '%s' ''' % (DDL_TABLE[2]))

# DROP_TABLE_K8S = ('''DROP TABLE IF EXISTS %s''' % DDL_TABLE[1])

DROP_FOREIGN_TABLE = ('''DROP FOREIGN TABLE IF EXISTS fdw.%s;''' % (table))

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

GET_SCHEMAS = ('''SELECT n.nspname AS "Name"
                            FROM pg_catalog.pg_namespace n
                                WHERE n.nspname !~ '^pg_' 
                            AND n.nspname not in ('information_schema','dba','cron','partman','pghero','repack','monitoring');''') 
      