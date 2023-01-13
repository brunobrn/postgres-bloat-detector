import psycopg2
from connections import *

# Get the migration version on main database and check if the version are the same.
def get_migration_version():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL Commands
        GET_MIGRATION_VERSION = ('''select max(migration_version) from dba.schema_migration ''')

        # Execute Commands
        cur.execute(GET_MIGRATION_VERSION)
        BD_MAIN_MIGRATION_VERSION = cur.fetchone()[0]

        # End Transaction
        cur.close()

        # Return boolean migration
        if BD_MAIN_MIGRATION_VERSION == migration_version:
            return True
        else: 
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# If the migration version is false, then we can execute the migration sql file
def exec_migration():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL Commands
        cur.execute(open("migration.sql", "r").read())

        # End transactions
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# function to execute the migration
def check_execute():
    if get_migration_version() == False:
        exec_migration()
        print("MIGRATION EXECUTADA")
        return True
    else:
        print("migration já instalada")
        return False

# finally, execute the program
check_execute()
