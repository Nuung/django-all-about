from django.db import models


class CheckedCrn(models.Model):
    registration_number = models.CharField(
        max_length=20, unique=True, blank=False, null=False, verbose_name="사업자등록번호"
    )
    is_closed = models.BooleanField(blank=False, null=False, verbose_name="사업자 폐업여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.registration_number}: {'closed' if self.is_closed else 'not close'} "
