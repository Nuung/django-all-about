#!/usr/bin/env bash

cd /app

pip install -r requirements.txt

CELERY_BEAT_LOG_ENABLED=True USE_DJANGO_LOGGING=False celery -A config.celery beat --loglevel DEBUG
