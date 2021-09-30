#!/bin/bash

# Startup all the containers without cache
docker-compose rm --all &&
docker-compose pull &&
docker-compose build --no-cache &&
docker-compose up -d --force-recreate

# Startup all the containers at once
# docker-compose up -d --build