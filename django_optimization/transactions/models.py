from django.db import models

from django_optimization.user.models import User


class BankInfo(models.Model):
    bank_code = models.CharField(max_length=4, primary_key=True)
    remark = models.TextField(
        blank=False,
        null=False,
        help_text="어떤 은행의 코드값인지 저장합니다.",
        verbose_name="은행",
    )

    def __str__(self) -> str:
        return f"{self.remark}, {self.bank_code}"


class AccountInfo(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_info",
    )
    bank_info = models.ForeignKey(
        BankInfo,
        on_delete=models.CASCADE,
        related_name="account_info",
    )
    account = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        help_text="사용자가 등록한 계좌 번호를 저장합니다.",
        verbose_name="계좌번호",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionType(models.TextChoices):
    CASH = "CA", "현금결제"
    VAN = "VA", "벤, 카드결제"
    PG = "PG", "PG 결제"
    OTHERS = "OT", "그 외"


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="transaction",
    )
    tran_date = models.DateTimeField(
        blank=False,
        null=False,
        help_text="사용자가 거래를 발생한 시간입니다.",
        verbose_name="거래발생시간",
    )
    pay_type = models.CharField(
        max_length=2,
        choices=TransactionType.choices,
        default=TransactionType.VAN,
        blank=False,
        null=False,
    )
    pay_platform = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        help_text="사용자가 거래를 발생시킨 플랫폼입니다. 실제 결제 모듈 플랫폼 또는 회사 정보를 저장합니다.",
        verbose_name="거래플랫폼",
    )
    amount_total = models.DecimalField(max_digits=12, decimal_places=0)
    amount_fee = models.DecimalField(max_digits=12, decimal_places=0)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
