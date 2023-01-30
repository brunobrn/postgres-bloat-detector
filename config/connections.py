import os
# Migration Version
migration_version=1

# main host
host        = os.environ['POSTGRES_MAIN_HOST']
dbname      = os.environ['POSTGRES_MAIN_DB']
user        = os.environ['POSTGRES_MAIN_USER']
password    = os.environ['POSTGRES_MAIN_PASSWORD']
port        = os.environ['POSTGRES_MAIN_PORT']

# k8s_bd_host
host_k8s        = os.environ['POSTGRES_K8S_HOST']
dbname_k8s      = os.environ['POSTGRES_K8S_DB']
user_k8s        = os.environ['POSTGRES_K8S_USER']
password_k8s    = os.environ['POSTGRES_K8S_PASSWORD']
port_k8s        = os.environ['POSTGRES_K8S_PORT']
