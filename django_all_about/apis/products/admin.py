
# django, drf lib
from django.contrib import admin

# app lib
from apis.products.models import ItemCategory, Items, SearchHistory

class ItemsChoiceInline(admin.StackedInline):
    model = Items
    extra = 3

class ItemCategoryAdmin(admin.ModelAdmin):
    inlines = [ItemsChoiceInline]


admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Items)
admin.site.register(SearchHistory)