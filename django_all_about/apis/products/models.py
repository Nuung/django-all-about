
# django, drf lib
from django.db import models
from django.conf import settings

class ItemCategory(models.Model):
    """
    - Items 모델의 카테고리 정의하는 Model
    - Items 의 정해진 분야를 세팅하기 위해 존재
    """
    category_name = models.CharField(max_length=4, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk}: {self.category_name}"


class Items(models.Model):
    """
    - 등록된 아이템 Model
    """
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    quantity = models.PositiveSmallIntegerField() # 음수값 불가능
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk}: {self.name}, {self.quantity}, {self.seller}"


class SearchHistory(models.Model):
    """
    - Item search history, 검색 이력을 위해 mongodb 활용해서 내역 저장 Model
    """
    search_query = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
