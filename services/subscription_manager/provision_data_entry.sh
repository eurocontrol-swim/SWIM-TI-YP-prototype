#!/bin/bash

env_update /app/provision_data/_config.yml /app/provision_data/config.yml && \

python /app/provision_data/init_db.py