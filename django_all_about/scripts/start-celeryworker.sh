#!/usr/bin/env bash

cd /app

pip install -r requirements.txt

USE_DJANGO_LOGGING=False celery -A config.celery worker -l INFO
