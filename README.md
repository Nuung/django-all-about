
# All About Django (almost)

> Django 로 가능한 다양한 형태의 실습, 테스트 케이스 
> complex - boilerplate 

- 우선 config, settings 값 등 환경 변수로 다뤄야 할 것들을 철저하게 단순 **테스트를 위해 파일에 같이 저장되어 있는 점 유의**
- DB 관련도 DBMS와 소통할 때 **no-auth 에 localhost 인 점도 꼭 유의**
- Django 에서 User와 Auth(Permission) 에 대한 부분은 철저하게 core만 사용함. 커스텀 없음
- exception에 대해서도 커스텀 없음.

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

### project init

- `git clone`
- `docker` 디렉토리로 가서 `docker-start.sh` 실행 (ex - `source docker-start.sh`)
- `python -m venv .venv` 가상환경은 직접 편한 방식으로 생성 
- `pip install -r requirements.txt`
- `python manage.py migrate`
- 디렉토리 만들기, `django_all_about >> logs` file logging을 사용하기 때문에 디렉토리 만들어줘야합니다.
- `python manage.py runserver` 정상 작동 테스트 후 exit
- 서버 러닝이 정상 작동 한다면, super user 생성하기, `python manage.py createsuperuser`
- `python manage.py collectstatic` 로 static file 생성 까지 진행
- `python manage.py runserver` 를 통해 localhost:8000/admin 으로 접속

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
            # 'username': '몽고DB 사용자 계정을 넣어주세요',
            # 'password': "몽고DB 사용자 비밀번호 넣어주세요",
            ...
            'username': 'nuung',
            'password': 'daa123!',
```

2. app 추가를 하려면
- 우선 apis 하위에 추가하려는 app의 디렉토리 (폴더)를 하나 추가한다.
- 그리고 `python manage.py startapp products ./apis/products` 커멘드로 세팅한다


## Case

### 1. 전체 프로젝트 도커라이징 및 다중 데이터베이스 활용하기
### 2. N:M 을 다루기
### 3. admin을 admin 답게 커스텀하기
### 4. Django middleware 만들기
### 5. DRF response, request 커스텀 자유롭게 하기
### 6. Model field index와 퍼포먼스 체커