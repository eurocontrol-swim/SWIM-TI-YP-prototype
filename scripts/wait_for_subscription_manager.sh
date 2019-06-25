#!/bin/bash

echo "Trying to connect to subscription_manager:8080"
while ! nc -z subscription_manager 8080;
do
    echo "Re-trying in 1 second";
    sleep 1;
done;

echo "Connected to subscription_manager!";