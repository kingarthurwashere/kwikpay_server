from django.db import models
from django.utils import timezone
from transactions.models import Transaction

# Create your models here.
class Order(models.Model):
    
        
    class Service(models.TextChoices):
        AIRTIME = 'Airtime', 'Airtime'
        DATA = 'Data', 'Data'
        ELECTRIC_BILL = 'Electricity Bill', 'Electricity Bill'
        
    
    user = models.ForeignKey('app_auth.User', on_delete=models.CASCADE, verbose_name='User')
    transaction = models.ForeignKey(Transaction(), on_delete=models.CASCADE, verbose_name='Transaction', null=True, blank=True)
    airtime_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Airtime Amount', null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Bill Amount', null=True, blank=True)
    data_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Data Amount', null=True, blank=True)
    mobile_number = models.CharField(max_length=50, verbose_name='Mobile Number', null=True, blank=True)
    meter_number = models.CharField(max_length=50, verbose_name='Meter Number', null=True, blank=True)
    operator = models.CharField(max_length=50, verbose_name='Operator')
    service = models.CharField(max_length=50, choices=Service.choices, verbose_name='Service')
    fulfilled = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='Total')
    
    
    def __str__(self):
        return self.user.username + " ordered " + self.service + " for " + str(self.total)
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=254, verbose_name='Email')
    get_offers = models.BooleanField(default=False, verbose_name='Get Offers')
    get_newsletters = models.BooleanField(default=False, verbose_name='Get Newsletters')
    
    
class UserQueries(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Subject')
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(max_length=254, verbose_name='Email')
    phone = models.CharField(max_length=50, verbose_name='Phone')
    query = models.TextField(verbose_name='Query')
    seen = models.BooleanField(default=False, verbose_name='Seen')
    answered = models.BooleanField(default=False, verbose_name='Answered')
    updated_at = models.CharField(max_length=50, verbose_name='Updated Date')
    
    
    
class Discount(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Percent')
    
   
class Package(models.Model):
    class PackageType(models.TextChoices):
        AIRTIME = 'Airtime', 'Airtime'
        DATA = 'Data', 'Data'
        BILL = 'Bill', 'Bill'
        
    name = models.CharField(max_length=50, verbose_name='Package Name')
    package_type = models.CharField(max_length=50, choices=PackageType.choices, verbose_name='Package Type')
    package_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Package Price', null=True, blank=True)
    
    
    def __str__(self):
        return self.name
    
class Setting(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.name