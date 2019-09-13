#!/bin/bash

source /secrets/broker/.env && \

env_update /app/swim_adsb/_config.yml /app/swim_adsb/config.yml && \

/usr/bin/python3 /app/swim_adsb/app.py
