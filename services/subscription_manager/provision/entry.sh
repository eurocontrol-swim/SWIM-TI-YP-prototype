#!/bin/bash

env_update /app/provision/_config.yml /app/provision/config.yml

echo "Waiting for DB..."

python /app/provision/provision_db.py

echo "Waiting for Broker..."

python /app/provision/provision_broker.py