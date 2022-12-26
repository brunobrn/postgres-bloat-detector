import psycopg2
import os
from config import host, dbname, user, password, port, table_name
from get_table_ddl import get_table_ddl
from exec_ddl import exec_ddl, ddl_table
from get_table_bloat_size import get_table_bloat_size
from drop_table_bloat import drop_table_bloat

# Create table as target table.
exec_ddl()

# Get the percentage of difference size
get_table_bloat_size()

# drop the table after tests
drop_table_bloat()