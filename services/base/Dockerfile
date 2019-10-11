FROM ubuntu

LABEL maintainer="SWIM EUROCONTROL <http://www.eurocontrol.int>"

RUN apt-get update --fix-missing && apt-get upgrade -y

RUN apt-get install gcc g++ cmake cmake-curses-gui uuid-dev \
    libssl-dev libsasl2-2 libsasl2-dev libsasl2-modules swig \
    python3 python3-dev python3-pip ruby-dev python3-qpid-proton \
    build-essential vim tree netcat pkg-config openssl libssl-dev \
    libffi-dev python-gevent gunicorn git -y

COPY env_update.sh /usr/bin/env_update

RUN chmod +x /usr/bin/env_update
