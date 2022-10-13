#!/bin/bash

docker-compose -f docker-compose.yml -p django-all-about-app stop
docker-compose -f docker-compose.yml -p django-all-about-app down
docker-compose -f docker-compose.yml -p django-all-about-app up -d