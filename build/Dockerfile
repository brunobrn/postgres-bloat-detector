FROM python:3

WORKDIR /get_bloat

COPY /build/requirements.txt requirements.txt

COPY /config /config
COPY /get_bloat /get_bloat/
COPY /queries /queries
COPY /migration /migration

RUN pip install --no-cache-dir -r requirements.txt
