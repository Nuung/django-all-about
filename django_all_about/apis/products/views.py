
# django, drf lib
from django.conf import settings
from django.shortcuts import render
from django.db import transaction, DatabaseError
from django.forms.models import model_to_dict
from django.contrib.auth.models import AnonymousUser
from rest_framework import (generics, status)
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# app lib
from apis.products.models import ItemCategory, Items, SearchHistory
from apis.products.serializers import ItemCategorySerializer, ItemsSerializer, SearchHistorySerializer

class ItemCategoryListCreateAPIView(generics.ListCreateAPIView):
    '''
    - ItemCategory 모델 GET ALL, CREATE (bulk) API
    '''
    queryset = ItemCategory.objects.all().order_by("-id")
    serializer_class = ItemCategorySerializer


class ItemsListCreateAPIView(generics.ListCreateAPIView):
    '''
    - Item 모델 GET ALL, CREATE (bulk) API
    '''
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemsSerializer


class SearchHistoryListAPIView(generics.ListAPIView):
    '''
    - Item 모델 GET ALL API
    '''
    queryset = SearchHistory.objects.all().order_by("-id")
    serializer_class = SearchHistorySerializer


@swagger_auto_schema(
    method='GET', 
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description='search query param', required=True, default="", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description='A page number within the paginated result set.', required=True, default=1, type=openapi.TYPE_INTEGER)
    ]
)  
@api_view(('GET',))
def search_item(request: Request):
    """
    - Item Model Search API
    """
    qry = request.GET.get("query")
    if not qry:
        return Response(status=status.HTTP_204_NO_CONTENT)

    user_pk = None if isinstance(request.user, (None, AnonymousUser)) else request.user.id

    try:
        # 트렌잭션
        with transaction.atomic():
            search_history = SearchHistorySerializer(data=dict(search_query=qry, user=user_pk))
            search_history.is_valid(raise_exception=True)
            search_history.save()
            
            # pagination setting
            searched_items = Items.objects.filter(name__icontains=qry).order_by("-id")
            paginator = PageNumberPagination()
            paginator.page_size = settings.DEFAULT_PAGE_SIZE
            result_page = paginator.paginate_queryset(searched_items, request)
            item_serializer = ItemsSerializer(result_page, many=True)
            return paginator.get_paginated_response(item_serializer.data)

    except DatabaseError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(('POST'))
# def buy_item(request: Request):
#     """
#     - Buy Item, create OrderRequest, OrderList from Item
#     """