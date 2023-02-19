import logging
import random

from celery import group

# django, drf lib
from django.core.cache import cache
from rest_framework import generics, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# app lib
from apis.test.tasks import check_registration_number_from_hometax
from apis.test.models import CheckedCrn, Product, Cart
from apis.test.serializers import (
    CheckedCrnSerializer,
    ProductSerializer,
    CartWithProductSerializer,
    CartSerializer,
    CartUpdateSerializer,
)
from batch.crawl_dev_quotes import DevQuote

logger = logging.getLogger(__name__)


class CheckedCrnListAPIView(generics.ListAPIView):
    """
    - CheckedCrn 모델 GET ALL API
    """

    queryset = CheckedCrn.objects.all().order_by("-id")
    serializer_class = CheckedCrnSerializer


class ProductListAPIView(generics.ListCreateAPIView):
    """
    - Product n Card GET ALL API & Create
    """

    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer


class CartListAPIView(generics.ListAPIView):
    """
    - Cart GET ALL API
    """

    queryset = Cart.objects.all().order_by("-id")
    serializer_class = CartWithProductSerializer


class CartCreateAPIView(generics.CreateAPIView):
    """
    - Cart Bulk Create API
    """

    queryset = Cart.objects.all().order_by("-id")
    serializer_class = CartSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        kwargs["many"] = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartBulkUpdateAPIView(viewsets.ModelViewSet):

    queryset = Cart.objects.all().order_by("-id")
    serializer_class = CartUpdateSerializer

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        kwargs["partial"] = True
        if kwargs.pop("pk", None):
            serializer = self.get_serializer(
                instance=self.get_object(), data=request.data, **kwargs
            )
        else:
            kwargs["many"] = isinstance(request.data, list)
            serializer = self.get_serializer(
                self.get_queryset(), data=request.data, **kwargs
            )
        serializer.is_valid(raise_exception=True)


@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(
            "query",
            openapi.IN_QUERY,
            description="검색할 사업자 등록 번호",
            required=True,
            default="",
            type=openapi.TYPE_STRING,
        ),
    ],
)
@api_view(("GET",))
def check_registration_number(request: Request):
    """
    - query에서 list로 넘어온 사업자 등록 번호들을 폐업 여부를 체크하는 API
    - celery task와 연동되서 비동기로 update 한다.
    """
    qry = request.GET.get("query")
    if not qry:
        return Response(status=status.HTTP_204_NO_CONTENT)

    qry_list = qry.split(",")
    ## as-is
    # for registration_number in qry_list:
    #     registration_number = registration_number.strip()
    #     check_registration_number_from_hometax.apply_async(args=[registration_number], kwargs={})
    ## to-be
    sub_task = [check_registration_number_from_hometax.si(q) for q in qry_list]
    logger.info("한글깨짐 테스트")
    logger.info(sub_task)

    group(sub_task)()

    return Response(
        dict(success=True, message="사업자 등록 번호를 조회합니다. 결과는 admin에서 확인해 주세요"),
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(
            "num",
            openapi.IN_QUERY,
            description="결과값 가져올 형태, 하나또는 전체",
            required=True,
            default="one",
            enum=["all", "one"],
            type=openapi.TYPE_STRING,
        ),
    ],
)
@api_view(("GET",))
def get_dev_quote(request: Request):
    """
    - cache에 저장된 DevQuote를 resturn
    - num (url querystring) [all or None] 값에 따라 하나 또는 전체 리턴한다.
    """
    num = request.GET.get("num", None)
    dev_quotes_list: list = cache.get("dev-quotes", None)
    results = dev_quotes_list if num == "all" else random.choice(dev_quotes_list)
    return Response(
        dict(success=True, results=results),
        status=status.HTTP_200_OK,
    )
