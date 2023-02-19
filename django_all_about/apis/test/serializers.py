import logging

# django, drf lib
from rest_framework import serializers

# app lib
from apis.test.models import CheckedCrn, Product, Cart

logger = logging.getLogger(__name__)

# class CheckedCrnSerializer(serializers.Serializer):
#     registration_number = serializers.CharField(max_length=20)
#     is_closed = serializers.BooleanField()
#     created_at = serializers.DateTimeField()
#     fixed_name = serializers.CharField(default="FIX")
#     updated_at = serializers.DateTimeField()


class CheckedCrnSerializer(serializers.ModelSerializer):
    is_long = serializers.SerializerMethodField()

    class Meta:
        model = CheckedCrn
        exclude = ("id",)

    def get_is_long(self, instance: CheckedCrn):
        if len(instance.registration_number) > 4:
            return "long"
        else:
            return "short"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    cart_set = CartSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ("id",)


class ProductOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartWithProductSerializer(serializers.ModelSerializer):
    product = ProductOnlySerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


# class CartListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         new_carts = [Cart(**item) for item in validated_data]
#         return Cart.objects.bulk_create(new_carts)


# class CartCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         exclude = ("id",)
#         list_serializer_class = CartListSerializer

import inspect
from rest_framework.exceptions import NotFound


class CartListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in enumerate(instances)}
        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]
        return result


class CartUpdateSerializer(serializers.ModelSerializer):
    # target_pk = serializers.IntegerField()

    def update(self, instance: Cart, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Cart
        fields = "__all__"
        update_lookup_field = "id"
        list_serializer_class = CartListSerializer
