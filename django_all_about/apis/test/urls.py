
# django, drf lib
from django.urls import path

# app lib
from apis.test.views import check_registration_number

urlpatterns = [

    path('check/', check_registration_number, name='check-registration-number'),

]