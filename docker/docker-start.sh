#!/bin/bash
echo ">> Django All About Project Docker Init"
docker-compose -f docker-compose.yml -p django-all-about-app stop
docker-compose -f docker-compose.yml -p django-all-about-app down
docker-compose -f docker-compose.yml -p django-all-about-app up -d
