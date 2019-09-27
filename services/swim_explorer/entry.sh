#!/bin/bash

env_update /app/swim_explorer/_config.yml /app/swim_explorer/config.yml && \

/usr/bin/python3 /app/swim_explorer/app.py

#gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind :5000 swim_explorer.app:flask_app
