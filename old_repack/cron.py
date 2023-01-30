import psycopg2
import os
from crontab import CronTab
from config import host, dbname, user, password, port, table_name, tuple_percent
from get_tuple_percent import get_tuple_percent
from execute_repack import execute_repack
from check_tuple import check_tuple

cron = CronTab(user='root')

job = cron.new(command='date > /opt/cron.log')

job.minute.every(1)
cron.write()