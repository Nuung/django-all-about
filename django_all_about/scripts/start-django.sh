#!/usr/bin/env bash

export DJANGO_SETTINGS_ENV="config.settings.local"

cd /app

pip install -r requirements.txt

python manage.py migrate
python manage.py migrate --database=orders
echo yes | python manage.py collectstatic

# fixture setting - db default value check
# ls **/fixtures/*.json 
python manage.py loaddata **/fixtures/*.json  # 이미 추가되어 있으면 추가 안됨

gunicorn config.wsgi:application --bind=0.0.0.0:8000 --workers=3 --timeout=60 --reload
# python manage.py runserver