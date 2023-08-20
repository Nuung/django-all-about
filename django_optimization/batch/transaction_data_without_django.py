import random
from time import time
from decimal import Decimal
from datetime import datetime, timedelta
from multiprocessing import Pool, Lock

import psycopg2
from psycopg2.extras import execute_values
import psycopg2.pool
import pytz

# 데이터베이스 연결 정보
DB_PARAMS = {
    "dbname": "daa-optimization-db",
    "user": "nuung",
    "password": "daa123!",
    "host": "localhost",
}
TZ = pytz.timezone("Asia/Seoul")
TODAY = datetime.now(TZ)
FEE_PERCENTAGE = random.uniform(0.05, 0.10)
PAT_TYPE_LIST = ["CA", "VA", "PG", "OT"]
PAT_PLATFORM_LIST = [
    "네이버",
    "쿠팡",
    "현장결제",
    "포장",
    "배달의민족",
    "요기요",
    "쿠팡이츠",
    "스마트스토어",
    "무신사",
    "아트모스",
    "나이키",
    "토스",
    "카카오",
    "구글",
    "앱스토어",
    "플레이스토어",
    "티머니",
    "기타",
]

# 데이터베이스 연결을 위한 Lock 객체 생성
DB_LOCK = Lock()

# 데이터베이스 연결 풀 생성
DB_POOL = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=16, **DB_PARAMS)


def make_random_datetime() -> datetime:
    # 특정 날짜 범위 설정 (예: 2022년 1월 1일부터 2023년 12월 31일까지)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)

    # 특정 날짜 범위 내에서 랜덤한 날짜 생성
    random_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )
    # 랜덤한 시간 생성
    random_time = datetime.min + timedelta(
        seconds=random.randint(0, (datetime.max - datetime.min).seconds)
    )
    # 랜덤한 날짜와 시간 합치기 & timezone 세팅
    return datetime.combine(random_date.date(), random_time.time(), tzinfo=TZ)


def make_transaction_dummy() -> list:
    transaction_bulk_list = list()
    for _ in range(10000):  # 1만 개
        user_id = random.randint(192, 211)
        tran_date = make_random_datetime()
        pay_type = random.choice(PAT_TYPE_LIST)
        pay_platform = random.choice(PAT_PLATFORM_LIST)
        amount_total = Decimal(str(random.randint(0, 100000)) + "0")
        amount_fee = amount_total * Decimal(str(FEE_PERCENTAGE))
        amount = amount_total - amount_fee
        created_at = TODAY
        transaction_bulk_list.append(
            (
                user_id,
                tran_date,
                pay_type,
                pay_platform,
                amount_total,
                amount_fee,
                amount,
                created_at,
            )
        )
    return transaction_bulk_list


def insert_into_bulk(idx: int):
    connection = DB_POOL.getconn()
    cursor = connection.cursor()

    random.seed()

    try:
        with DB_LOCK:
            datas = make_transaction_dummy()
            query = """
                INSERT INTO transactions_transaction (user_id, tran_date, pay_type, pay_platform, amount_total, amount_fee, amount, created_at)
                VALUES %s;
            """
            execute_values(cursor, query, datas)
            connection.commit()
    except Exception as exc:
        print(f"insert_into_bulk error >> {exc}, {exc.__class__}")
        connection.rollback()
    finally:
        cursor.close()
        # 연결을 풀에 반환
        DB_POOL.putconn(connection)


if __name__ == "__main__":
    start_time = time()

    with Pool() as pool:
        pool.map(insert_into_bulk, range(64))  # 64회 실행

    end_time = time()
    execution_time = end_time - start_time
    print(execution_time)
