from datetime import datetime
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotAcceptable
from rest_framework.request import Request
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # 한 페이지에 보여줄 항목 수 설정
    page_size_query_param = "page_size"  # 페이지 크기 조절을 위한 파라미터 이름 설정
    max_page_size = 1000  # 최대 페이지 크기 설정


class TransactionsListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by("-id")
    serializer_class = TransactionSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["pay_platform", "pay_type"]

    @method_decorator(cache_page(60 * 5))  # 5분 동안 응답 캐싱
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if order_by := self.request.query_params.get("order_by", None):
            if order_by == "pay":
                queryset = queryset.order_by("pay_type", "pay_platform")
            elif order_by == "date":
                queryset = queryset.order_by("tran_date")
            else:
                raise NotAcceptable(f"order_by cannot be {order_by}")

        if date_search := self.request.query_params.get("date_search", None):
            date_search = datetime.strptime(date_search, "%Y-%m-%d")
            start_datetime = date_search.replace(hour=0, minute=0, second=0)
            end_datetime = date_search.replace(hour=23, minute=59, second=59)
            queryset = queryset.filter(tran_date__range=(start_datetime, end_datetime))

        return queryset
