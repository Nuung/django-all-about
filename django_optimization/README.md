# Django Optimization App

> `requirements.txt` file은 `django_all_about` 를 공유해서 사용합니다.
> 참고로 ***도커라이징 안되어 있으며 온프레미스 형태로*** 진행합니다.

## 🔥 Getting Started

#### 1. `git clone`

#### 2. `django_all_about` app의 docker - `postgresql(default)` 를 공유합니다.
- 아니면 DB만 `localhost:5432` & `daa-optimization-db` 로 세팅하면 됩니다.
- 만약 daa app의 docker psql을 그대로 사용한다면 아래 create database만 진행해주세요!

```sql
CREATE DATABASE "daa-optimization-db";
```

- 자세한 사항은 `config/settings.py` 참조

#### 3. `python manage.py migrate` 으로 table 세팅

- 이후 아래 쿼리로 기본 table 세팅 여부 체크

```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

#### 4. `python manage.py runserver` 로 정상 러닝 체크

- 해당 app은 logging등 어떤 추가 커스텀 세팅 없고, 비즈니스로직 및 최적화에만 집중하고 있습니다.
- app은 `user` 와 `transactions` app만 사용하고 있습니다.


#### 5. blog post follow up

-