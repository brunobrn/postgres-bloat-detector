from config import schema, table
from subprocess import call

call(["python", "py_automator/01_create_type_oban.py", schema, table])
call(["python", "py_automator/02_create_fdw.py", schema, table])
call(["python", "py_automator/03_import_fdw_into_k8s.py", schema, table])
call(["python", "py_automator/05_copy_table.py", schema, table])
call(["python", "py_automator/06_get_size_diff.py", schema, table])

# import create_type_oban_00 public oban_jobs

# exec(open('01_create_type_oban.py').read())

# from create_type_oban_01 import create_type_oban_jobs
# os.environ['PYTHONINSPECT'] = 'True'
# table_name=sys.argv[1:len(sys.argv)]
# schema=table_name[0]
# table=table_name[1]
# print(table)

# def exec_py():
#     table_name=sys.argv[1:len(sys.argv)]
#     schema=table_name[0]
#     table=table_name[1]
#     return schema, table # schema index 0 and table index 1

# schema1=exec_py[0]
# table1=exec_py[1]
# exec_py()
# create_type_oban = __import__("01_create_type_oban")
# create_fdw = __import__("02_create_fdw")
# import_fdw_into_k8s = __import__("03_import_fdw_into_k8s")