#!/bin/bash

data_provision() {
    echo "Data provisioning to Subscription Manager..."
    echo -e "============================================\n"
    docker-compose up -d subscription-manager-provision
    echo ""
}

start_services() {
    echo "Starting up SWIM..."
    echo -e "===================\n"
    docker-compose up -d web-server subscription-manager swim-adsb swim-explorer
    echo ""
}


stop_services_with_clean() {
    echo "Stopping SWIM..."
    echo -e "================\n"
    docker-compose down
    echo ""
}

stop_services() {
    echo "Stopping SWIM..."
    echo -e "================\n"
    docker-compose stop
    echo ""
}

build() {
    echo "Building images..."
    echo -e "==================\n"
    # build the base image upon which the swim services will depend on
    docker build -t swim-base -f ./services/base/Dockerfile ./services/base
    docker build -t swim-base.conda -f ./services/base/Dockerfile.conda ./services/base
    docker-compose build
    echo ""
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
    echo ""
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
