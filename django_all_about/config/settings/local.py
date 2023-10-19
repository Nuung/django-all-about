"""
Django settings for django_all_about project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

import environ
from celery.beat import crontab

from config.logging.develop_logging import DEVELOP_LOGGING

# root 디렉토리를 "django_all_about" 으로 세팅해 둠
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# https://pypi.org/project/python-environ/
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# reading .env file
environ.Env.read_env()

DEBUG = env("DEBUG")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")


# 접근 허용 호스트 - all
ALLOWED_HOSTS = ["*"]

# 로깅 세팅
Path(f"{BASE_DIR}/logs").mkdir(parents=True, exist_ok=True)
DJANGO_LOGGING_PATH = f"{BASE_DIR}/logs/daa-django.log"
DEVELOP_LOGGING["handlers"]["file"]["filename"] = DJANGO_LOGGING_PATH
LOGGING = DEVELOP_LOGGING  # django logging

# celery logging
CELERY_LOG_LEVEL = "INFO"
CELERY_LOG_PATH = f"{BASE_DIR}/logs/daa-celery.log"
CELERY_BEAT_LOG_PATH = f"{BASE_DIR}/logs/daa-celery-beat.log"
CELERY_BEAT_FLAG = env.bool("CELERY_BEAT_FLAG", False)

# ==================================================================== #
#                     설치된 앱, 사용하는 앱 config                         #
# ==================================================================== #

INSTALLED_APPS = [
    # Default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",  # https://django-extensions.readthedocs.io/
    # Celery
    "django_celery_beat",
    # Prometheus
    "django_prometheus",
    # other adds / extentions
    "corsheaders",  # cors, django-cors-headers
    "drf_yasg",  # swagger, drf-yasg
    "django_filters",  # queryset filter, django-filter
    "debug_toolbar",  # debug (side tool bar), django-debug-toolbar
    # for rest-auth
    "allauth",
    "allauth.account",
    "rest_auth.registration",
    # DRF
    "rest_framework",  # djangorestframework
    "rest_framework_simplejwt",  # drf jwt
    "rest_framework_simplejwt.token_blacklist",
    # 추가한 API, APPs
    "apis.test",
    "apis.user",
    "apis.products",
    "apis.orders",
]

MIDDLEWARE = [
    # Prometheus for Django
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # default
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # other adds / extentions
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug tool bar
    "corsheaders.middleware.CorsMiddleware",
    # custom middleware
    "config.custom_middleware.ViewProcessTimeMiddleware",
    # Prometheus for Django
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# route되는 url에 대한 설정파일
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"  # 언어 - 국가 설정
USE_TZ = True  # 장고 시간대
TIME_ZONE = "Asia/Seoul"  # 시간대
USE_I18N = True  # 국제화 -> Internationalization
USE_L10N = True  # 지역화 -> localization


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_PAGE_SIZE = 10

# Debug toolbar config
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}


# ==================================================================== #
#                  file system (static) config                         #
# ==================================================================== #

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# ==================================================================== #
#                       DRF, JWT config                                #
# ==================================================================== #
# https://www.django-rest-framework.org/

AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "config.pagination.DefaultPagination",  # 커스텀 페이지네이션 사용 선언
    "PAGE_SIZE": DEFAULT_PAGE_SIZE,
    # 'EXCEPTION_HANDLER': 'config.exceptions.base.custom_exception_handler',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "apis.user.serializers.CustomRegisterSerializer"
}

REST_USE_JWT = True

# JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,  # True로 설정할 경우, refresh token을 보내면 새로운 access token과 refresh token이 반환된다.
    "BLACKLIST_AFTER_ROTATION": True,  # True로 설정될 경우, 기존에 있던 refresh token은 blacklist가된다
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "user.User",
    # 'JTI_CLAIM': 'jti',
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

ACCOUNT_ADAPTER = "apis.user.adapter.AccountAdapter"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

# ==================================================================== #
#                       DataBase config                                #
# ==================================================================== #

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

## db라우터
DATABASE_ROUTERS = [
    "config.order_dbrouter.MultiDBRouter",
    "config.dbrouter.MultiDBRouter",
]

# # for not docker
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "daa-postgres-db",
#         "USER": "nuung",
#         "PASSWORD": "daa123!",
#         "HOST": "daa-postgres",
#         "PORT": "5432",
#     },
#     "read": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "daa-postgres-db",
#         "USER": "nuung",
#         "PASSWORD": "daa123!",
#         "HOST": "daa-postgres-sub",
#         "PORT": "5432",
#     },
#     "orders": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "daa-postgres-order-db",
#         "USER": "nuung",
#         "PASSWORD": "daa123!",
#         "HOST": "localhost",
#         "PORT": "5432",
#     },
# }
DATABASES = {
    "default": env.db("MAIN_DB_URL"),
    "read": env.db("READ_DB_URL"),
    "orders": env.db("ORDER_DB_URL"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["orders"]["ATOMIC_REQUESTS"] = True

# ==================================================================== #
#                           CORS config                                #
# ==================================================================== #

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]


# ==================================================================== #
#                     django file size config                          #
# ==================================================================== #


# 단위 BYTE
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 31457280  # 30mb 제한
DATA_UPLOAD_MAX_MEMORY_SIZE = 31457280  # 30 mb 제한 - request body limit
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # the maximum number of parameters GET, POST

# 2.5메가 이하의 파일의 경우 장고에서는 전체를 메모리에 올려버립니다. 다른의미로 메모리에서 읽고 디스크에 쓰는 행동이므로 상대적으로 빠릅니다.
# 만약 파일 용량이 default값보다 클 경우 임시 디렉토리에 저장합니다.
FILE_UPLOAD_MAX_MEMORY_SIZE = 31457280  # 30mb, 얘 보다 큰 사이즈 경우 메모리 말고 임시 디렉토리 저장


# ==================================================================== #
#                     celery setting - config                          #
# ==================================================================== #

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")  # redis를 MQ로 사용, 브로커서버 주소
BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]  # celery가 message를 받을때 type
CELERY_TASK_SERIALIZER = "json"  # 시리얼라이징(직렬화) 하는 타입
CELERY_TIMEZONE = TIME_ZONE  # TIME_ZONE = 'Asia/Seoul'    # 시간대
CELERY_TASK_TRACK_STARTED = True  #
CELERY_TASK_TIME_LIMIT = 30 * 60  # 프로세스가 도는 시간, 다른 거는 프로세스가 실행하기까지 (그때까지 실행안하면 안됨)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

# 아래 설정값 해줘야 BEAT TIME ZONE DIFF 에러를 안뱉어냄
# https://blog.fearcat.in/a?ID=01500-db2867b7-fdf9-4cb0-93fe-105cc446dbb2
DJANGO_CELERY_BEAT_TZ_AWARE = USE_TZ  # celery beat의 장고 시간대 사용 여부
# CELERY_BEAT_TIMEZONE = TIME_ZONE                    # celery beat TIME_ZONE = 'Asia/Seoul'


# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#std-setting-beat_schedule
CELERY_BEAT_SCHEDULE = {
    "crawling-dev-quotes-and-update": {
        "task": "batch.crawl_dev_quotes.crawl_dev_quotes_batch",
        "schedule": crontab(minute=0, hour="0"),
        "options": {
            "expires": 2 * 60,  # 2 min
        },
    },
}


# ==================================================================== #
#                    django cache - redis config                       #
# ==================================================================== #

# https://tute.io/how-to-cache-django-rest-framework-with-redis
# https://github.com/jazzband/django-redis
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
