
from django.db import models

class ItemCategory(models.Model):
    """
    - Items 모델의 카테고리 정의하는 Model
    - Items 의 정해진 분야를 세팅하기 위해 존재
    """
    category_name = models.CharField(max_length=4, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Items(models.Model):
    """
    - 등록된 아이템 Model
    """
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    quantity = models.PositiveSmallIntegerField() # 음수값 불가능

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)