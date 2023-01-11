#!/usr/bin/env bash

cd /app

USE_DJANGO_LOGGING=False celery -A config.celery worker -l INFO
