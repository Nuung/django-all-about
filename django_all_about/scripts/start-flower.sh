#!/usr/bin/env bash

cd /app

pip install -r requirements.txt

celery flower \
    --app=config.celery \
    --broker="${CELERY_BROKER_URL}" \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
