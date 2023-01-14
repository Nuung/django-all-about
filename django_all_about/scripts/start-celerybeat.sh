#!/usr/bin/env bash
export CELERY_BEAT_FLAG=true
cd /app

pip install -r requirements.txt

celery -A config.celery beat --loglevel DEBUG
