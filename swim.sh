#!/bin/bash

data_provision() {
    docker-compose up -d subscription-manager-provision
}

start_services() {
    docker-compose up -d web-server \
                         subscription-manager \
                         swim-adsb \
                         swim-explorer
}

stop_services() {
    docker-compose down
}

build() {
    docker-compose build
}


ACTION=${1}

case ${ACTION} in
  build)
    build
    ;;
  start)
    echo "Starting up SWIM"
    start_services
    ;;
  stop)
    echo "Stopping SWIM"
    stop_services
    ;;
  provision)
    echo "Data provisioning to Subscription Manager"
    data_provision
    ;;
  *)
    echo Invalid value for ACTION.
    exit 1
    ;;
esac
