#!/bin/bash

docker run -p 1883:1883 eclipse-mosquitto:latest /usr/sbin/mosquitto -c /mosquitto-no-auth.conf