# django, drf lib
from rest_framework import serializers

# app lib
from apis.orders.models import OrderAddress, OrderRequest, OrderList


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        exclude = ("id",)


class OrderRequestSerializer(serializers.ModelSerializer):
    order_address = OrderAddressSerializer(read_only=True)

    class Meta:
        model = OrderRequest
        exclude = ("id",)


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        exclude = ("id",)


class CreateOrderRequestSerializer(serializers.Serializer):

    pass
