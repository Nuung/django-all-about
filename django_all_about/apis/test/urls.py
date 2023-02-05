# django, drf lib
from django.urls import path

# app lib
from apis.test.views import check_registration_number, get_dev_quote

urlpatterns = [
    path("check/", check_registration_number, name="check-registration-number"),
    path("dev-quote/", get_dev_quote, name="get-dev-quote"),
]
