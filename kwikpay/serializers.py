from pyexpat import model
from rest_framework import serializers
from .models import Transaction, AirtimeTransaction, ZesaTransactions

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AirtimeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirtimeTransaction
        fields = '__all__'

class ZesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZesaTransactions
        fields = '__all__'