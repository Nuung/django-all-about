import os
import logging
from logging.handlers import TimedRotatingFileHandler

from celery import (
    Celery,
)  # celery status = PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS
from celery.signals import (
    after_setup_logger,
    after_setup_task_logger,
)  # https://stackoverflow.com/questions/48289809/celery-logger-configuration

from config.logging.develop_logging import CeleryJSONFormatter

# 환경 변수 세팅 - project 명의 setting 값 이용
env = os.environ.get("DJANGO_SETTINGS_ENV", "config.settings.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env)
# BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')


# Project Name으로 Celery app생성
app = Celery("config")

# 문자열로 등록한 이유는 Celery Worker가 Windows를 사용할 경우
# 객체를 pickle로 묶을 필요가 없다는 것을 알려주기 위함입니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# 추가 설정 사항 오버라이트 하기
app.conf.update(result_expires=3600, enable_utc=False, timezone="Asia/Seoul")

# celery가 task를 자동으로 찾게 세팅해주기 -> @share_task & @app.task 어노테이션만 달아주면 됨
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# celery & celery beat logging setting
# signal 활용
@after_setup_logger.connect
@after_setup_task_logger.connect
def setup_logger(
    sender=None,
    logger=None,
    loglevel=None,
    logfile=None,
    format=None,
    colorize=None,
    **kwargs,
):
    from django.conf import settings

    formatter = CeleryJSONFormatter()

    # Console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # File
    celery_log_path = (
        str(settings.CELERY_BEAT_LOG_PATH)
        if settings.CELERY_BEAT_FLAG
        else str(settings.CELERY_LOG_PATH)
    )
    file_handler = TimedRotatingFileHandler(
        filename=celery_log_path, when="D", interval=1, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Set Handler
    celery_log_level = logging.getLevelName(settings.CELERY_LOG_LEVEL)

    # Replace default Celery console handler to avoid duplicated console log message.
    logger.handlers[0] = stream_handler
    logger.addHandler(file_handler)
    logger.setLevel(celery_log_level)


if __name__ == "__main__":
    app.start()
