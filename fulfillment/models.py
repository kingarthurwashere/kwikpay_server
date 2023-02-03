from django.db import models
from main.models import Order
from app_auth.models import User

# Create your models here.

class TrackTransaction(models.Model):
    
    class ExceptionType(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        SERVICE_DOWN = 'Service Down', 'Service Down'
        SERVICE_ERROR = 'Service Error', 'Service Error'
        LIMIT_ERROR = 'Limit Error', 'Limit Error'
        INSUFFICIENT_BALANCE = 'Insufficient Balance', 'Insufficient Balance'
        
    class TransactionStatus(models.TextChoices):
        OPEN = "Opened", "Opened"
        CLOSED = "Closed", "Closed"
        ON_HOLD = "On Hold", "On Hold"
        
    class ClosedReason(models.TextChoices):
        RETRY_REACHED = "Retry Reached", "Retry Reached"
        STILL_OPEN = "Still Open", "Still Open"
        WENT_THROUGH = "Went Through", "Went Through"
        
        
    order = models.ForeignKey(Order(), on_delete=models.DO_NOTHING, verbose_name="Order")
    user = models.ForeignKey(User(), on_delete=models.DO_NOTHING, verbose_name="User")
    request = models.TextField(verbose_name="Request", default="" )
    response = models.TextField(verbose_name="Response", default= "")
    retry_times = models.IntegerField(verbose_name="Retry Times", default=0)
    max_retries = models.IntegerField(verbose_name="Max Retries", default=10)  
    timeout = models.IntegerField(verbose_name="Timeout", default=2)
    timeout_multiplier = models.IntegerField(verbose_name="Timeout Multiplier", default=2)
    exception_name = models.CharField(max_length=100, choices=ExceptionType.choices, verbose_name="Exception Name")
    status = models.CharField(max_length=100, choices=TransactionStatus.choices, default=TransactionStatus.OPEN.label, verbose_name="Transaction Status")
    closed_reason = models.CharField(max_length=100, choices=ClosedReason.choices, default=ClosedReason.STILL_OPEN.label, verbose_name="Closed Reason")
