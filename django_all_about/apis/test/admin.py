# django, drf lib
from django.contrib import admin

# app lib
from apis.test.models import CheckedCrn, Product, Cart

admin.site.register(CheckedCrn)
admin.site.register(Product)
admin.site.register(Cart)
