FROM python:3

WORKDIR /get_bloat

COPY get_bloat/requirements.txt requirements.txt

COPY /get_bloat .

RUN pip install --no-cache-dir -r requirements.txt
