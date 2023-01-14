#!/usr/bin/env bash
export CELERY_BEAT_FLAG=false
cd /app

pip install -r requirements.txt

celery -A config.celery worker -l INFO
