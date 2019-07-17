#!/bin/bash

data_provision() {
    echo -e "Data provisioning to Subscription Manager...\n"
    docker-compose up -d subscription-manager-provision
}

start_services() {
    echo -e "Starting up SWIM...\n"
    docker-compose up -d web-server subscription-manager swim-adsb swim-explorer
}


stop_services_with_clean() {
    echo -e "Stopping SWIM...\n"
    docker-compose down
}

stop_services() {
    echo -e "Stopping SWIM...\n"
    docker-compose stop
}

build() {
    echo -e "Building images...\n"
    docker build -t swim-base ./services/base  # build the base image upon which the swim services will depend on
    docker-compose build
}

status() {
    docker ps
}

usage() {
    echo -e "Usage: swim.sh [COMMAND] [OPTIONS]\n"
    echo "Commands:"
    echo "    provision       Provisions the Subscription Manager with initial data (users)"
    echo "    start           Starts up all the SWIM services"
    echo "    start --prov    Starts up all the SWIM services after Provisioning the Subscription Manager with initial data"
    echo "    stop            Stops all the services"
    echo "    stop --clean    Stops all the services and cleans up the containers"
    echo "    status          Displays the status of the running containers"
}

if [[ $# -lt 1 || $# -gt 2  ]]
then
    usage
    exit 0
fi

ACTION=${1}

case ${ACTION} in
    build)
        build
        ;;
    start)
        if [[ ! -z ${2} ]]
        then
            EXTRA=${2}

            case ${EXTRA} in
                --prov)
                    data_provision
                    ;;
                *)
                    echo -e "Invalid argument\n"
                    usage
                    exit 1
                    ;;
            esac
        fi

        start_services
        ;;
    stop)
        if [[ ! -z ${2} ]]
        then
            EXTRA=${2}

            case ${EXTRA} in
                --clean)
                    stop_services_with_clean
                    ;;
                *)
                    echo -e "Invalid argument\n"
                    usage
                    exit 1
                    ;;
            esac
            exit 0
        fi
        stop_services
        ;;
    provision)
        data_provision
        ;;
    status)
        status
        ;;
    help)
        usage
        ;;
    *)
        echo -e "Invalid action\n"
        usage
        exit 1
        ;;
esac
