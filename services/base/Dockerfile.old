FROM continuumio/miniconda3:latest

LABEL maintainer="SWIM EUROCONTROL <http://www.eurocontrol.int>"

RUN apt-get update -y; apt-get upgrade -y

RUN apt-get install build-essential vim tree netcat pkg-config openssl libssl-dev libsasl2-2 libsasl2-dev libsasl2-modules libffi-dev python-gevent gunicorn  -y

RUN conda update -n base -c defaults conda

COPY env_update.sh /usr/bin/env_update

RUN chmod +x /usr/bin/env_update
