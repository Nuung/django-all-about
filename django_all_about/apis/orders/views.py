# python lib
from typing import Any

# django, drf lib
from django.db import transaction, DatabaseError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

# app lib
from apis.orders.models import OrderAddress, OrderRequest, OrderList
from apis.orders.serializers import (
    OrderAddressSerializer,
    OrderRequestSerializer,
    OrderListSerializer,
)
from apis.products.models import Items
from apis.products.serializers import ItemsSerializer


class OrderRequestListAPIView(generics.ListAPIView):
    """
    - OrderRequest GET ALL from reuqest user API
    """

    serializer_class = OrderRequestSerializer

    def get_queryset(self):
        return (
            OrderRequest.objects.filter(user=self.request.user)
            .select_related("order_address")
            .order_by("-id")
        )


@api_view(("POST",))
def create_order_request(request: Request):
    """
    - OrderRequest를 새로 만드는건 아래 다음 step을 따른다.
    1. 최근에 작성한 OrderAddress 가 있다면, pk 를 받고, 최초 주문 또는 새로운 생성이라면 OrderAddress 를 새로 만든다
    2. OrderRequest를 만든 후 User, OrderAddress fk 연결 한다. (not save)
    3. OrderList를 (2)에서 만든 OrderRequest fk 기반으로 request body로 온 item pk 만큼 만든다.
    4. OrderRequest를 save 한다. 이 비즈니스 로직은 하나의 transaction 이다.
    """

    request_data = request.data.copy()
    if request_data.get("order_address"):
        new_order_address = get_object_or_404(
            OrderAddress, pk=request_data.get("order_address"), user=request.user
        )
    else:
        if not request_data.get("order_address_data", None):
            return Response(
                {"error": "주소를 입력해 주세요"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_order_address = OrderAddress(
            user=request.user, order_address=request_data.pop("order_address_data")
        )
        new_order_address.save()

    try:
        # 트렌잭션
        with transaction.atomic():
            new_order_request = OrderRequest()
            new_order_request.user = request.user
            new_order_request.order_address = new_order_address

            item_list: list[dict] = request_data.pop("item_list")
            for item in item_list:
                new_order_list = OrderList()
                new_order_list.order_request = new_order_request
                new_order_list.item = item.get("id")
                new_order_list.quantity = item.get("quantity")
                new_order_list.save()

            new_order_request_serializer = OrderRequestSerializer(new_order_request)
            new_order_request_serializer.is_valid(raise_exception=True)
            new_order_request_serializer.save()

        return Response(
            new_order_request_serializer.data, status=status.HTTP_201_CREATED
        )

    except DatabaseError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
