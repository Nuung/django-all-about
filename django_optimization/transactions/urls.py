from django.urls import path

from transactions.views import TransactionsListAPIView

urlpatterns = [
    path("", TransactionsListAPIView.as_view(), name="transaction-list-apiview"),
]
