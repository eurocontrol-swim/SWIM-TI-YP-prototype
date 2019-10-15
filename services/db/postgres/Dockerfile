FROM postgres:11

RUN apt-get update && apt-get install nano

ENV DB_NAME='smdb'

COPY ./services/db/postgres/data/postgresql.conf /etc/postgresql.conf

RUN mkdir /var/lib/postgresql/secrets/

RUN chmod 600 /var/lib/postgresql/secrets/server_key.pem

COPY ./secrets/postgres/* /var/lib/postgresql/secrets/

RUN chown -R postgres:postgres /var/lib/postgresql/secrets/