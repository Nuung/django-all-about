# django, drf lib
from django.urls import path

# app lib
from apis.test.views import (
    CheckedCrnListAPIView,
    ProductListAPIView,
    CartListAPIView,
    CartCreateAPIView,
    CartBulkUpdateAPIView,
    check_registration_number,
    get_dev_quote,
)

urlpatterns = [
    path(
        "checked-crn/", CheckedCrnListAPIView.as_view(), name="checked-crn-list-apiview"
    ),
    path("products/", ProductListAPIView.as_view(), name="product-list-apiview"),
    path("carts/", CartListAPIView.as_view(), name="cart-list-apiview"),
    path("cart-bulk/", CartCreateAPIView.as_view(), name="cart-create-apiview"),
    path(
        "cart-bulk-update/",
        CartBulkUpdateAPIView.as_view({"put": "list"}),
        name="cart-update-apiview",
    ),
    path("check/", check_registration_number, name="check-registration-number"),
    path("dev-quote/", get_dev_quote, name="get-dev-quote"),
]
