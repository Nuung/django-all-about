#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.conf import settings
from django.db.utils import OperationalError


def main():
    """Run administrative tasks."""
    env = os.environ.get("DJANGO_SETTINGS_ENV", "config.settings.local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # try:
    #     execute_from_command_line(sys.argv)
    # except OperationalError:  # db connection error
    #     settings.DATABASES = {
    #         "default": {
    #             "ENGINE": "django.db.backends.postgresql",
    #             "NAME": "daa-postgres-db",
    #             "USER": "nuung",
    #             "PASSWORD": "daa123!",
    #             "HOST": "localhost",
    #             "PORT": "5432",
    #         },
    #         "orders": {
    #             "ENGINE": "django.db.backends.postgresql",
    #             "NAME": "daa-postgres-order-db",
    #             "USER": "nuung",
    #             "PASSWORD": "daa123!",
    #             "HOST": "localhost",
    #             "PORT": "5432",
    #         },
    #     }
    #     execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
