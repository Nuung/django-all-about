'''
file 핸들러에 사용된 항목은 다음과 같다.

level - 출력 레벨로 INFO를 사용
filters - DEBUG=False인 운영 환경에서 사용
class - 파일 핸들러로 RotatingFileHandler 사용, RotatingFileHandler는 파일 크기가 설정한 크기보다 커지면 파일 뒤에 인덱스를 붙여서 백업한다. 이 핸들러의 장점은 로그가 무한히 증가되더라도 일정 개수의 파일로 롤링(Rolling)되기 때문에 로그 파일이 너무 커져서 디스크가 꽉 차는 위험을 방지할 수 있다.
filename - 로그 파일명은 logs 디렉터리에 mysite.log로 설정
maxBytes - 로그 파일의 최대 크기는 5MB로 설정
backupCount - 롤링되는 파일의 개수를 의미한다. 총 5개의 로그 파일로 유지되도록 설정했다.
formatter - 포맷터는 standard를 사용
'''
import logging

from celery._state import get_current_task
from json_log_formatter import JSONFormatter

TARGET_ATTR = ["levelname", "name", "module", "funcName", "lineno", "filename", "pathname", "created"]

class CustomisedJSONFormatter(JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra.update(
            {
                attr_name: record.__dict__[attr_name]
                for attr_name in record.__dict__
                if attr_name in TARGET_ATTR
            }
        )
        extra['message'] = message or record.message
        request = extra.pop('request', None)
        if request:
            extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
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
    'version': 1,
    'disable_existing_loggers': False,

    # root 값 변경해줘야함 실제 환경에서는 
    "root": {
        "level": "INFO", 
        "handlers": ["file"]
    },
    "formatters": {
        "default_formatter": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        'json': {
            '()': CustomisedJSONFormatter,
        }
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
            # 'class': 'logging.handlers.RotatingFileHandler', # console이랑 같이 쓸때
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*10,
            "backupCount":5,
            # 'filename': BASE_DIR / 'logs/django_all_about.log',
            "formatter": "json",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    }
}


# view파일에서 아래와 같이 로깅하면 된다 
# import logging
# logger = logging.getLogger('pybo')
# logger.info("INFO 레벨로 출력")
