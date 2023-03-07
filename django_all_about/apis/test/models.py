from django.db import models
from django.utils.translation import gettext_lazy as _

from apis.user.models import User


class CheckedCrn(models.Model):
    registration_number = models.CharField(
        max_length=20, unique=True, blank=False, null=False, verbose_name="사업자등록번호"
    )
    is_closed = models.BooleanField(blank=False, null=False, verbose_name="사업자 폐업여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.registration_number}: {'closed' if self.is_closed else 'not close'} "


class Product(models.Model):
    name = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="제품 이름"
    )
    price = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"[{self.name}] {self.price}원"


class CartStatus(models.TextChoices):
    DEFAULT = "DE", _("Default value")
    DONE = "DN", _("End of purchase value")
    CANCEL = "CN", _("Cancel or delete value")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False
    )
    status = models.CharField(
        max_length=2,
        choices=CartStatus.choices,
        default=CartStatus.DEFAULT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk} {self.user.name}, {self.user.email} 유저가 {self.product} 담음"
