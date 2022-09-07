from django.contrib import admin

from .models import Transaction, ZesaTransactions,  AirtimeTransaction


admin.site.register(Transaction)
admin.site.register(ZesaTransactions)
admin.site.register(AirtimeTransaction)
