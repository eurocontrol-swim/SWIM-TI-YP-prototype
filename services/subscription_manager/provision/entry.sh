#!/bin/bash

env_update /app/provision/_config.yml /app/provision/config.yml && \

python /app/provision/provision_db.py && \

python /app/provision/provision_broker.py