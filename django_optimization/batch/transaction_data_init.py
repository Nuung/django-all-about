import random
from decimal import Decimal
from datetime import datetime, timedelta

from django.utils import timezone

from user.models import User
from transactions.models import Transaction, TransactionType

TODAY = timezone.localdate()
FEE_PERCENTAGE = random.uniform(0.05, 0.10)
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
    result = datetime.combine(random_date.date(), random_time.time())
    result = timezone.make_aware(result, timezone=timezone.get_current_timezone())
    return result


transaction_bulk_list = list()

for _ in range(2000):
    # 랜덤 값들
    transaction_type_choices = [choice[0] for choice in TransactionType.choices]
    random_transaction_type = random.choice(transaction_type_choices)
    target_user = User.objects.all().order_by("?").first()
    target_platform = random.choice(PAT_PLATFORM_LIST)

    # 랜덤한 거래 액 값 생성
    random_total = Decimal(str(random.randint(0, 100000)) + "0")
    random_fee = random_total * Decimal(str(FEE_PERCENTAGE))
    random_amount = random_total - random_fee

    transaction_bulk_list.append(
        Transaction(
            user=target_user,
            tran_date=make_random_datetime(),
            pay_type=random_transaction_type,
            pay_platform=target_platform,
            amount_total=random_total,
            amount_fee=random_fee,
            amount=random_amount,
        )
    )

res = Transaction.objects.bulk_create(transaction_bulk_list)
print(f"[{TODAY}] {len(res)} 개의 Transaction bulk create")
