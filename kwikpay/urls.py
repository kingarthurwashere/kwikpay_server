from django.urls import include, path
from .views import (
    TransactionList, TransactionDetail,
    AirtimeTransactionList, AirtimeTransactionDetail,
    ZesaTransactionsList, ZesaTransactionDetail)

urlpatterns = [
    path('transactions/', TransactionList.as_view(), name='transactions'),
    path('transactions/<int:id>/', TransactionDetail.as_view(), name='transaction'),

    path('airtime-transactions/', AirtimeTransactionList.as_view(), name='airtime-transactions'),
    path('airtime-transactions/<int:id>/', AirtimeTransactionDetail.as_view(), name='airtime-transaction'),

    path('zesa-transactions/', ZesaTransactionsList.as_view(), name='zesa-transactions'),
    path('zesa-transactions/<int:id>/', ZesaTransactionDetail.as_view(), name='zesa-transaction'),
]