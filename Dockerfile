FROM python:3

WORKDIR /py_automator

COPY py_automator/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt update
RUN apt -y install postgresql-13-repack

# CMD [ "python" ]
ENTRYPOINT ["tail", "-f", "py_automator/requirements.txt"]