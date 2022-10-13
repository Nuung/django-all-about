
# django, drf lib
from django.contrib import admin

# app lib
from apis.products.models import ItemCategory, Items, SearchHistory

admin.site.register(ItemCategory)
admin.site.register(Items)
admin.site.register(SearchHistory)