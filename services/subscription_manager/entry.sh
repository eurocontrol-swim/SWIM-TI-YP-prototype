#!/bin/bash

source /secrets/.env && \

env_update /app/subscription_manager/_config.yml /app/subscription_manager/config.yml && \

gunicorn -w 1 --bind :8080 subscription_manager.wsgi:app