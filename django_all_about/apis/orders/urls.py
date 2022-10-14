
# django, drf lib
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# app lib
from apis.orders.views import OrderRequestListAPIView, create_order_request

urlpatterns = [
    path('order-requests/', OrderRequestListAPIView.as_view(), name='OrderRequest-ListAPIView'),
    path('order-request/', csrf_exempt(create_order_request), name='OrderRequest-CreateAPIView-fbv'),
]