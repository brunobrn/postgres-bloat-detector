FROM python:3

WORKDIR /py_automator

COPY py_automator/requirements.txt requirements.txt
COPY py_automator/.pgpass /root/.pgpass

COPY . .

RUN chmod -R 0600 /root/.pgpass
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
# RUN apt -y install sleepenh
RUN apt -y install postgresql-13-repack

# CMD [ "python", "py_automator/sleep.py" ]
# ENTRYPOINT ["psql -h 10.9.33.4 -U dbapy_database_username -d dbapy_database -c "select pg_sleep(5000)""]