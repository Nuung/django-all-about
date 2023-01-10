#!/usr/bin/env bash

USE_DJANGO_LOGGING=False celery -A app.config.celery worker -l INFO
