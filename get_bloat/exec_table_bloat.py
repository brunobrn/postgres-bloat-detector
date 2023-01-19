import psycopg2
from table_bloat import *
from connections import *

#exec functions
create_type_oban_jobs()
create_fdw_k8s()
import_fdw_k8s()

copy_table_to_k8s()
# Do the math to get the real size difference of the table
main_table_size = get_size_diff_rds()
k8s_table_size = get_size_diff_k8s()
percentage_diff = (main_table_size-k8s_table_size)/main_table_size*100
print("The percentage diff is: ",(main_table_size-k8s_table_size)/main_table_size*100)
drop_table_bloat()

### ----------------------------------- ###

# Insert data on monitoring table
def insert_bloat_monitor():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()
        
        # SQL Commands
        INSERT_BLOAT = ('''INSERT INTO dba.bloat_monitor(
        table_name, schema, size_original, size_k8s, percentage_diff, inserted_at)
        VALUES ('%s', '%s', %s, %s, '%s', current_timestamp);''' % (table, schema, main_table_size, k8s_table_size, percentage_diff))

        # Execute commands
        cur.execute(INSERT_BLOAT)

        # End transaction
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('-------------------------------------------------------------') 

insert_bloat_monitor()
