
import os
from celery import Celery # celery status = PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS

# 환경 변수 세팅 - project 명의 setting 값 이용
env = os.environ.get('DJANGO_SETTINGS_ENV', 'config.settings.local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env)
# BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')


# Project Name으로 Celery app생성
app = Celery('config')

# 문자열로 등록한 이유는 Celery Worker가 Windows를 사용할 경우 
# 객체를 pickle로 묶을 필요가 없다는 것을 알려주기 위함입니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 추가 설정 사항 오버라이트 하기
app.conf.update(
    result_expires=3600,
    enable_utc = False,
    timezone = 'Asia/Seoul'
)

app.autodiscover_tasks() # celery가 task를 자동으로 찾게 세팅해주기 -> @share task 어노테이션만 달아주면 됨
# app.conf.broker_url = BASE_REDIS_URL

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


if __name__ == '__main__':
    app.start()
