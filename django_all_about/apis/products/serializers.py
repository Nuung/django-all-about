# django, drf lib
from rest_framework import serializers

# app lib
from apis.products.models import ItemCategory, Items, SearchHistory


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        exclude = ("id",)


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        exclude = ("id",)


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        exclude = ("id",)
