from django.shortcuts import render
from rest_framework import generics
from .models import Transaction, AirtimeTransaction, ZesaTransactions
from .serializers import (
    TransactionSerializer,
    AirtimeTransactionSerializer,
    ZesaTransactionSerializer)


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class AirtimeTransactionList(generics.ListCreateAPIView):
    queryset = AirtimeTransaction.objects.all()
    serializer_class = AirtimeTransactionSerializer


class AirtimeTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirtimeTransaction.objects.all()
    serializer_class = AirtimeTransactionSerializer


class ZesaTransactionsList(generics.ListCreateAPIView):
    queryset = ZesaTransactions.objects.all()
    serializer_class = ZesaTransactionSerializer


class ZesaTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZesaTransactions.objects.all()
    serializer_class = ZesaTransactionSerializer
