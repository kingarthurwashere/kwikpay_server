from django.db import models
from django.utils import timezone


# Create your models here.

class Transaction(models.Model):
    class Status(models.TextChoices):
        WAITING_PAYMENT = 'Waiting Payment', 'Waiting Payment'
        CANCELLED = 'Cancelled', 'Cancelled'
        PAYMENT_SUCCESS = 'Payment Success', 'Payment Success'
        PAYMENT_FAILED = 'Payment Failed', 'Payment Failed'
        IN_TRANSIT = 'In Transit', 'In Transit'
        DELIVERED = 'Delivered', 'Delivered'

    gateway = models.CharField(max_length=50, verbose_name='Gateway')
    transaction_id = models.CharField(max_length=100, verbose_name='Transaction ID', blank=True, null=True)
    transaction_object = models.TextField(null=True, blank=True)
    refunded = models.BooleanField(default=False, verbose_name='Refunded')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Amount', null=True,
                                       blank=True)
    customer_email = models.EmailField(max_length=255, verbose_name='Customer Email', blank=True, null=True)
    payment_date = models.CharField(max_length=200, verbose_name='Payment Date', blank=True, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, verbose_name='Status')
    paid = models.BooleanField(default=False, verbose_name='Paid')

    def __str__(self):
        return "#" + str(self.id) + self.payment_date


class AirtimeTransaction(models.Model):
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Status')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount', null=True, blank=True)
    error_message = models.CharField(max_length=255, verbose_name='Error Message', null=True, blank=True)
    agent_reference = models.CharField(max_length=255, verbose_name='Agent Reference', null=True, blank=True)
    data = models.TextField(verbose_name='Data', null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Discount', null=True, blank=True)
    final_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Final Balance', null=True,
                                        blank=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Initial Balance', null=True,
                                          blank=True)
    recharge_id = models.CharField(max_length=255, verbose_name='Recharge ID', null=True, blank=True)
    reply_code = models.CharField(max_length=255, verbose_name='Reply Code', null=True, blank=True)
    reply_message = models.CharField(max_length=255, verbose_name='Reply Message', null=True, blank=True)
    sms = models.CharField(max_length=255, verbose_name='SMS', null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Wallet Balance', null=True,
                                         blank=True)
    window = models.CharField(max_length=255, verbose_name='Window', null=True, blank=True)
    created_at = models.CharField(max_length=255, verbose_name='Created At', null=True, blank=True,
                                  default=timezone.now)


class ZesaTransactions(models.Model):
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Status')
    error_message = models.CharField(max_length=255, verbose_name='Error Message', null=True, blank=True)
    agent_reference = models.CharField(max_length=255, verbose_name='Agent Reference', null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Discount', null=True, blank=True)
    recharge_id = models.CharField(max_length=255, verbose_name='Recharge ID', null=True, blank=True)
    reply_code = models.CharField(max_length=255, verbose_name='Reply Code', null=True, blank=True)
    reply_message = models.CharField(max_length=255, verbose_name='Reply Message', null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Wallet Balance', null=True,
                                         blank=True)
    meter = models.CharField(max_length=255, verbose_name='Meter', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    account_name = models.CharField(max_length=255, verbose_name='Account Name', null=True, blank=True)
    tokens = models.TextField(verbose_name='Tokens', null=True, blank=True)
    created_at = models.CharField(max_length=255, verbose_name='Created At', null=True, blank=True,
                                  default=timezone.now)
