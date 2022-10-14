
# django, drf lib
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            is_superuser=True,
            **extra_fields
        )
        user.is_admin = True  # User model 내 is_admin
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    - User table model
    """
    email = models.EmailField(  # 사용자 ID (email format)
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=50)  # 사용자 이름 
    is_active = models.BooleanField(default=True)  # 활성 비활성 - 탈퇴시 비활성 (core)
    is_admin = models.BooleanField(default=False)  # UserManager 참고 (core)
    date_joined = models.DateTimeField(auto_now_add=True)  # 회원가입일, (core)
    objects = UserManager()  # 재정의 된 UserManager 사용 선언

    USERNAME_FIELD = 'email'  # email을 ID 필드로 사용 선언
    REQUIRED_FIELDS = ['name']  # 사용자 이름은 필수 필드

    def __str__(self):
        return self.email

    # Django core에서는 staff 값 사용 -> admin 값 사용하게
    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    class Meta:
        app_label = 'user'
