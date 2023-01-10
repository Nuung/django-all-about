
# All About Django (almost)

> [블로그 글](https://velog.io/@qlgks1/series/Django-Basic-to-Advanced) 과 같이 본다면 더 이해하기 쉽다.
> Django 로 가능한 다양한 형태의 실습, 테스트 케이스 
> complex - boilerplate 

- 우선 config, settings 값 등 환경 변수로 다뤄야 할 것들을 철저하게 단순 **테스트를 위해 파일에 같이 저장되어 있는 점 유의**
- DB 관련도 DBMS와 소통할 때 **auth, localhost 인 점도 꼭 유의** , mongodb 는 auth가 optional
- User는 refresh 없는 1년 유효 jwt token (django simplejwt), 인가는 drf 기본 Authorization만 사용
  - User 대충하려다가 조금 token 세팅 빡세게 해버렸다..
- admin (super user)는 특별한 custom 없이 진행
- exception은 커스텀 없이 진행

## Infra & Requirements

- Django
- DRF (Django RestFrameWork)
- Gunicorn (wsgi)
- Celery, Celery Beat
- Redis
- Postgresql
- Mongodb
- Nginx

## Getting Start

### requirements

1. git
2. docker & docker compose

### project init & start

1. `git clone`
2. `docker` 디렉토리로 가서 `docker-start.sh` 실행 (ex - `source docker-start.sh`)
- 상대 경로 등의 설정으로 인해 **꼭 해당 디렉토리로 가서 shell을 실행**시키자.
- `docker` 경로 내부에 ***러닝 스크립트 관련 scripts***, `requirements.txt` 가 있으니 필참
- 초기 실행시 main image가 될 **dda-django** 이미지 빌드하고 러닝하는데 시간이 조금 걸릴 것 이다.

3. 
- `python -m venv .venv` 을 통해 직접 local 환경 구성을 해서 진행을 해도 괜찮고
- `pip install -r requirements.txt`

- `python manage.py migrate`
- `python manage.py migrate --database=orders` 다중 데이터베이스 세팅으로 꼭 해주셔야 합니다.
- 디렉토리 만들기, `django_all_about >> logs` file logging을 사용하기 때문에 디렉토리 만들어줘야합니다.
- `python manage.py runserver` 정상 작동 테스트 후 exit
- 서버 러닝이 정상 작동 한다면, super user 생성하기, `python manage.py createsuperuser`
- `python manage.py collectstatic` 로 static file 생성 까지 진행
- `python manage.py runserver` 를 통해 http://localhost/admin 으로 접속 
  - 8000으로 바인딩했으면서 왜 80으로 가냐? docker - nginx conf 참조, 리버스 프록시 세팅 모두 되어있음
- 이후 업데이트 시 `scripts > server-run.sh` 파일을 source 명령어로 러닝하면 된다. (데이터 세팅 때문에 최초 1회는 꼭 필요하다)

### detail config

1. mongo user 만들기
- mongo container shell 접근
- mongo --host 127.0.0.1 --port 29019
```shell
use admin
db.createUser(
  {
    user: "nuung",
    pwd:  "daa123!",
    roles: [ { role: "root", db: "admin" } ]
  }
)
db.runCommand('usersInfo')
```
- 이후 `settings > local.py` 의 DB 값 에서 다음 값을 바꿔주면 된다.
```python
  ...
  # 'username': '몽고DB 사용자 계정을 넣어주세요',
  # 'password': "몽고DB 사용자 비밀번호 넣어주세요",
  'username': 'nuung',
  'password': 'daa123!',
  ...
```

2. app 추가를 하려면
- 우선 apis 하위에 추가하려는 app의 디렉토리 (폴더)를 하나 추가한다.
- 그리고 `python manage.py startapp products ./apis/products` 커멘드로 세팅한다
- `urls.py` 와 `serializers.py` 추가로 세팅해서 사용하면 된다. 
- `apps.py` 세팅값도 살짝 바꾸는게 좋은데, 이미 있는 것을 참고하길 바란다.

3. 분리된 config > setting 에서 `manage.py shell` 에 접근할 때에는 `python manage.py shell --settings=config.settings.local` 와 같이 option을 추가해 줘야 한다. 

4. 기본적인 url 들은 아래와 같다
- `localhost` : main, index but not used
- `localhost/admin` ; django의 핵심, admin 페이지 이다.
- `localhost/swagger/` : 스웨거는 꼭 들어가 보길, 말그대로 swagger로 API 정리되어있는 문서다. drf와 drf_yasg 의 합작이다.
- `localhost/api/...` : API endpoint 의 pre-fix로 "api" 가 붙는다. 

5. `python manage.py shell --setting=config.settings.local < ./apis/products/item_dump_generator.py` 커멘드를 통해 dump item generating을 할 수 있다.

6. django 파일 빈번하게 바꾸면서 테스트할 꺼라면, django를 도커라이징에서 제외하고 사용하는 것을 추천 (기본 세팅)

## Case

### 1. 전체 프로젝트 도커라이징 및 다중 데이터베이스 활용하기
- `config > dbrouter.py` 부분과 `config > settings > local.py` 에서 Database setting 부분을 참조해 보자
- model에 `app_lable` 을 붙이는 것과 migrate 진행시 database option을 주는 것

### 2. 모든 api는 unit test와 coverage와 함께
- model moking 하기, 특히 user model 과 같은 경우

### 3. N:M 을 다루기
- OrderRequest 에서 출발을 해서, 해당 유저가 구매요청(OrderRequest)에 해당하는 모든 item과 seller를 찾아보자
- `OrderRequest 1<-N OrderList N->1 item N->1 seller` 

### 4. admin을 admin 답게 커스텀하기
- 기존에 있는 admin을 좀 더 admin이 활용할 수 있게 custom 하기
- createsuperuser 로 만들어지는 superuser 회원가입 template 만들기
- mongodb에 있는 dump data를 보는 template 만들기

### 5. Django middleware 만들기
- `HttpRequest -> HttpResponse` 이 처리 구간에서 time library의 `process_time_ns` 함수를 활용해서 응답 헤더에 추가해 보자.
- `config > custom_middleware.py` 를 확인해 보자.

### 6. DRF response, request 커스텀 자유롭게 하기
-

### 7. Model field index와 퍼포먼스 체커
- 최적화로 들어가는 Django query
- API 스트레스 체크 및 최적화, 캐싱처리하기
  - celery로 실시간 검색어 순위를 비동기적으로 계속해서 변경 및 저장
  - 그 순위 5순위까지 검색 결과값 item search result json를 redis에 캐싱처리하기 
  - 계속되는 최적화 및 캐싱처리로 체크


### 8. redis + celery worker / celery beat & redis pub n sub 구조 활용하기
- django -> redis -> celery beat / celery worker (if result) -> redis
- django -> redis message queue (producing) <- queue consumer action
  - 여기서 message queue는 redis를 대체하여 여타 다른 메시징 큐를 사용해도 무방하다.
- 위 2가지를 활용하기, 자세한 내용은 아래 블로그 글들로 대신한다.
- [Django Celery - async worker celery & redis (message que) basic](https://velog.io/@qlgks1/Django-Celery-MQ-message-que)
- [Django Redis - caching, scheduling (task), pub/sub message que](https://velog.io/@qlgks1/Django-Redis-caching-scheduling-task-messaging-celery-async-worker)