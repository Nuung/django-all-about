
# django, drf lib
from django.urls import path

# app lib
from apis.products.views import ItemCategoryListCreateAPIView, ItemsListCreateAPIView, SearchHistoryListAPIView, search_item

urlpatterns = [

    path('item-categorys/', ItemCategoryListCreateAPIView.as_view(), name='ItemCategory-ListCreateAPIView'),
    path('items/', ItemsListCreateAPIView.as_view(), name='Items-ListCreateAPIView'),
    
    path('items/search/', search_item, name='Items-SearchAPI'),
    path('items/search-history/', SearchHistoryListAPIView.as_view(), name='SearchHistory-ListAPIView'),

]