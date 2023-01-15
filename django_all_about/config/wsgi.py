"""
WSGI config for django_all_about project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get("DJANGO_SETTINGS_ENV", "config.settings.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env)

application = get_wsgi_application()
