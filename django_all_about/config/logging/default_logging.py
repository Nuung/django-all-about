'''
version
version은 고정값 1을 사용해야 한다. 만약 다른 값을 입력하면 ValueError가 발생한다. 이 값은 의미 없어 보일 수도 있지만, logging 모듈이 업그레이드되어도 현재 설정을 보장해 주는 안전장치이다.

disable_existing_loggers
disable_existing_loggers 항목은 False로 설정했다. 만약 True로 설정하면 기존에 설정된 로거들을 사용하지 않게 된다. 파이보도 기존에 설정된 로거를 비활성화할 특별한 이유가 없으므로 False로 설정할 것이다.

filters
필터는 특정 조건에서 로그를 출력하거나 출력하지 않기 위해서 사용된다. require_debug_false 필터는 DEBUG=False인지를 판단하는 필터이고, require_debug_true는 DEBUG=True 인지를 판단하는 필터이다. 조건 판단을 위해 각각 django.utils.log.RequireDebugFalse와 django.utils.log.RequireDebugTrue 클래스를 호출하여 DEBUG 항목의 True, False를 판단한다.

formatters
포맷터에는 로그를 출력할 형식을 정의한다. 포맷터에 사용된 항목은 다음과 같다.

server_time - 서버의 시간
message - 출력내용
handlers
핸들러는 로그의 출력 방법을 정의한다. 다음은 DEFAULT_LOGGING 설정에 등록된 핸들러이다.

console - 콘솔에 로그를 출력한다. 로그 레벨이 INFO 이상이고 DEBUG=True일 때만 로그를 출력한다.
django.server - python manage.py runserver로 작동하는 개발 서버에서만 사용하는 핸들러로 콘솔에 로그를 출력한다.
mail_admins - 로그 내용을 이메일로 전송하는 핸들러로, 로그 레벨이 ERROR 이상이고 DEBUG=False 일때만 로그를 전송한다. 핸들러 사용 조건은 환경설정 파일에 ADMINS라는 항목을 추가하고 관리자 이메일을 등록해야 한다(예: ADMINS = ['pahkey@gmail.com']). 그리고 이메일 발송을 위한 SMTP 설정도 필요하다.
loggers
로그를 출력하는 프로그램에서 사용하는 로거(logger)의 이름을 의미한다. DEFAULT_LOGGING 설정에는 다음과 같은 로거들이 등록되어 있다.

django - 장고 프레임워크가 사용하는 로거로 로그 레벨이 INFO 이상일 경우에만 로그를 출력한다.
django.server - 개발 서버가 사용하는 로거로 로그 레벨이 INFO 이상일 경우에만 로그를 출력한다. 'propagate': False의 의미는 django.server가 출력하는 로그를 django 로거로 전달하지 않는다는 의미이다. 만약 'propagate': True로 설정하면 최상위 패키지명이 django로 동일하기 때문에 django.server 하위 패키지에서 출력하는 로그가 django.server 로거에도 출력되고 django 로거에도 출력되어 이중으로 출력될 것이다.
로그 레벨

로그 레벨은 다음과 같이 5단계로 구성된다. 각 단계는 logging.debug, logging.info, logging.warning, logging.error, logging.critical 함수로 출력할 수 있다.

1단계 DEBUG: 디버깅 목적으로 사용
2단계 INFO: 일반 정보를 출력할 목적으로 사용
3단계 WARNING: 경고 정보를 출력할 목적으로(작은 문제) 사용
4단계 ERROR: 오류 정보를 출력할 목적으로(큰 문제) 사용
5단계 CRITICAL: 아주 심각한 문제를 출력할 목적으로 사용
설명에서 짐작할 수 있듯이 로그 레벨의 순서는 다음과 같다.

DEBUG < INFO < WARNING < ERROR < CRITICAL
로그는 설정한 레벨 이상의 로그만 출력된다. 예를 들어 핸들러나 로거의 로그 레벨을 INFO로 설정하면 DEBUG 로그는 출력되지 않고 INFO 이상의 로그만 출력된다. 즉, logging.debug로 출력하는 로그는 출력되지 않고 logging.info, logging.warning, logging.error, logging.critical로 출력한 로그만 출력된다는 말이다. 만약 로그 레벨을 ERROR로 설정한다면 logging.error, logging.critical로 출력한 로그만 출력될 것이다.

장고의 DEFAULT_LOGGING 설정을 알아보았다. 장고 로깅에 대한 보다 자세한 내용은 아래의 URL을 참고하도로 하자.

장고 로깅 : docs.djangoproject.com/en/3.0/topics/logging
'''

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
