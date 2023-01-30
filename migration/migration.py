import psycopg2
import sys

sys.path.insert(1, '/config')

from connections import *

# Get the migration version on main database and check if the version are the same.

def check_if_table_migration_exists():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL Commands

        CHECK_TABLE = ('''SELECT EXISTS (
                            SELECT FROM 
                                pg_tables
                            WHERE 
                                schemaname = 'dba' AND 
                                tablename  = 'schema_migration');''')

        cur.execute(CHECK_TABLE)
        BOOL_TABLE = cur.fetchone()[0]

        if BOOL_TABLE == True:
            print('-------------------------------------------------------------') 
            print('MIGRATION TABLES ALREADY CREATED')
        elif BOOL_TABLE == False:
            print('-------------------------------------------------------------') 
            print('MIGRATION TABLES NOT CREATED - STARTING MIGRATION')
        else:
            print('-------------------------------------------------------------') 
            print('ERROR - BOOLEAN NOT WORKING ON MIGRATION.PY')

        # End transactions
        conn.commit()
        cur.close()
        return BOOL_TABLE

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()

def get_migration_version():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL Commands
        GET_MIGRATION_VERSION = ('''select case when max(migration_version) is null then 0
                                        else max(migration_version) end from dba.schema_migration''')

        # Execute Commands
        cur.execute(GET_MIGRATION_VERSION)
        BD_MAIN_MIGRATION_VERSION = cur.fetchone()[0]

        # End Transaction
        cur.close()

        # Return boolean migration
        if BD_MAIN_MIGRATION_VERSION == migration_version:
            return BD_MAIN_MIGRATION_VERSION
        else: 
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# If the migration version is false, then we can execute the migration sql file
def migration_00001():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL Commands
        cur.execute(open("/migration/migrations/00001_create_schema.sql", "r").read())
        cur.execute(open("/migration/migrations/00001_create_tables.sql", "r").read())
        cur.execute(open("/migration/migrations/00001_create_function.sql", "r").read())
        cur.execute(open("/migration/migrations/00001_create_view.sql", "r").read())
        cur.execute(open("/migration/migrations/00001_manage_owner.sql", "r").read())
        cur.execute(open("/migration/migrations/00001_migration_version.sql", "r").read())

        # End transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# finally, execute the program

def exec_migration_00001():
    if check_if_table_migration_exists() == False:
        print('EXECUTING MIGRATION TO VERSION 1')
        migration_00001()
        print('MIGRATION EXECUTED WITH SUCCESS')
        print('-------------------------------------------------------------') 
        return True
    elif get_migration_version() == 0:
        print('MIGRATION VERSION IS 0, EXECUTING MIGRATION TO VERSION 1')
        migration_00001()
        print('MIGRATION EXECUTED WITH SUCESS TO VERSION 1')
        print('-------------------------------------------------------------') 
        return True
    else:
        print('MIGRATION ALREADY OK')
        print('-------------------------------------------------------------') 
        return False

exec_migration_00001()