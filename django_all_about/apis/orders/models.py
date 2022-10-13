
# django, drf lib
from django.db import models
from django.contrib.auth.models import User

# app lib
from apis.products.models import Items

class OrderRequest(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'orders'

class OrderList(models.Model):

    order_request = models.ForeignKey(OrderRequest, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField() # 음수값 불가능
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'orders'