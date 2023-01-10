#!/usr/bin/env bash

CELERY_BEAT_LOG_ENABLED=True USE_DJANGO_LOGGING=False single-beat celery -A app.config.celery beat --loglevel DEBUG
