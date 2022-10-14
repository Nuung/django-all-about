
# django, drf lib
from django.db import models
from django.conf import settings

# app lib
from apis.products.models import Items


class OrderAddress(models.Model):
    """
    - 해당 구매요청의 배송지를 저장하는 OrderAddress Model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_address = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'orders'

class OrderRequest(models.Model):
    """
    - User의 구매 요청 자체만 저장하는 OrderRequest Model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE)
    ORDER_STATUS = (
        ('INIT', '구매요청한 상태'),
        ('PROCESSING', '구매처리중인 상태'),
        ('COMPLETED', '구매완료된 상태'),
        ('CANCEL', '취소된 상태')
    )
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default="INIT")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'orders'

class OrderList(models.Model):
    """
    - User의 구매 요청에 해당하는 모든 아이템을 기록해 두는 OrderList Model
    """
    order_request = models.ForeignKey(OrderRequest, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField() # 음수값 불가능, 주문 총 수량
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'orders'

