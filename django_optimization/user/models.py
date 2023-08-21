from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    nick_name = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text="사용자가 등록한 닉네임, 별칭입니다.",
        verbose_name="닉네임",
    )
    profile_img = models.URLField(
        help_text="사용자가 등록한 프로필 사진입니다.",
        verbose_name="프로필사진",
        default="https://picsum.photos/160",
    )
    profile_desc = models.TextField(
        blank=True,
        null=True,
        help_text="사용자가 등록한 프로필 설명입니다.",
        verbose_name="프로필",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        related_name="user",
        null=True,
    )
    name = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        verbose_name="사용자 이름",
    )
    phone = PhoneNumberField(
        help_text="사용자가 등록한 전화번호입니다.",
        verbose_name="사용자 전화번호",
        region="KR",
        unique=True,
    )
    inflow = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="사용자 유입경로",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
