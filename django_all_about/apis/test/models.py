import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apis.user.models import User


class CrnOpenedManager(models.Manager):
    def all_closed(self):
        return self.get_queryset().filter(is_closed=False)


class CheckedCrn(models.Model):
    registration_number = models.CharField(
        max_length=20, unique=True, blank=False, null=False, verbose_name="사업자등록번호"
    )
    is_closed = models.BooleanField(blank=False, null=False, verbose_name="사업자 폐업여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CrnOpenedManager()

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


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, "title") and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PostStatus(models.TextChoices):
    DEFAULT = "DE", _("Default")
    PUBLIC = "PU", _("Public")
    PRIVATE = "PR", _("Private")


class PublicPostMixin:
    def pre(self):
        if self.status is not PostStatus.PUBLIC:
            return

    def set_public(self):
        self.status = PostStatus.PUBLIC.value
        self.save()


class PrivatePostMixin:
    def set_private(self):
        self.status = PostStatus.PRIVATE.value
        self.save()


class Post(TimestampMixin, SlugMixin, PublicPostMixin, PrivatePostMixin):
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=2,
        choices=PostStatus.choices,
        default=PostStatus.DEFAULT,
    )
    body = models.TextField()
    objects = models.Manager()

    @property
    def is_old(self):
        if datetime.datetime.now().day - self.created_at.day > 1:
            return True
        return False

    def __str__(self):
        return self.title
