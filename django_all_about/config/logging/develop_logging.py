import logging

from celery._state import get_current_task
from json_log_formatter import JSONFormatter

TARGET_ATTR = [
    "levelname",
    "name",
    "module",
    "funcName",
    "lineno",
    "filename",
    "pathname",
    "created",
]


class CustomisedJSONFormatter(JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra.update(
            {
                attr_name: record.__dict__[attr_name]
                for attr_name in record.__dict__
                if attr_name in TARGET_ATTR
            }
        )
        extra["message"] = message or record.message
        request = extra.pop("request", None)
        if request:
            extra["x_forward_for"] = request.META.get("X-FORWARD-FOR")
        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)
        else:
            extra["exc_info"] = None
        return extra


class CeleryJSONFormatter(CustomisedJSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra = super().json_record(message, extra, record)
        # Update task info.
        task = get_current_task()
        if task and task.request:
            extra["task_id"] = task.request.id
            extra["task_name"] = task.name
        else:
            extra["task_id"] = None
            extra["task_name"] = None
        return extra


DEVELOP_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # root 값 변경해줘야함 실제 환경에서는
    "root": {"level": "INFO", "handlers": ["file"]},
    "formatters": {
        "default_formatter": {
            "format": (
                "%(asctime)s [%(levelname)-8s] " "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": CustomisedJSONFormatter,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file": {
            "level": "INFO",
            # 'filters': ['require_debug_false'],
            # 'class': 'logging.handlers.RotatingFileHandler',
            # "maxBytes": 1024*1024*10,
            # "backupCount":5,
            # 'filename': BASE_DIR / 'logs/django_all_about.log',
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "formatter": "json",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


# 특정 로깅을 하고 싶은 경우, 다음과 같이 로깅하면 된다
# import logging
# logger = logging.getLogger('django')
# logger.info("INFO 레벨로 출력")
