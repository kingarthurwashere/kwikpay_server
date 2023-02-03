from django.test import TestCase
from fulfillment.models import TrackTransaction
from main.models import Order
from transactions.models import Transaction

from faker import Faker
from app_auth.models import User
from app_utils.helpers import get_custom_request, get_timestamp
import json
from munch import Munch
from fulfillment.tasks import *
fake = Faker()

# Create your tests here.
class ZesaFulfillmentTestCase(TestCase):
    
    def setUp(self):
        
        response = Munch({
            'Status': 'pending',
            'ReplyCode': 4, 
            'ReplyMsg': 'Pending ZESA Token Purchase of $675.00 for 01620187847. \r\nPlease check transaction in 5 minutes to see if status has been updated by Service Provider.\r\nThank you for choosing HOT Recharge', 
            'WalletBalance': 0.0, 
            'Amount': 675.0, 
            'ProviderFees': 0.0, 
            'Discount': 0.0, 
            'Meter': '01620187847', 
            'AccountName': '', 
            'Address': '', 
            'Tokens': [], 
            'AgentReference': '', 
            'RechargeID': 111591104, 
            'CustomerInfo': 
                Munch({
                    'Reference': '', 
                    'CustomerName': '', 
                    'Address': '', 
                    'MeterNumber': '01620187847'
                    })
        })
        
        user = User.objects.create_user(
            fake.name(), 
            "johnwick@mail.com", 
            fake.password(), 
            first_name=fake.first_name(), 
            last_name=fake.last_name())
        
        new_trans  = Transaction.objects.create(
            gateway = "unknown",
            transaction_id = user.username +"-" + get_timestamp(),
            status = Transaction.Status.WAITING_PAYMENT.label,
            total_amount = 3.00,
        )
        
        new_trans.save()
        order = Order.objects.create(
            user=user, 
            transaction= new_trans,
            operator="Econet", 
            mobile_number="0778548832",
            service=Order.Service.ELECTRIC_BILL.label,
            meter_number= "01620187847",
            total= 3.00,
            airtime_amount=3.00
        )
        
        self.exception_transaction = TrackTransaction.objects.create(
            order = order,
            user = user,
            request =json.dumps(Munch({
                "host": "127.0.0.1:8000",
                "scheme": "http",
                "email": "madechangu.takunda@gmail.com",
                "user_id": 36
            })),
            response = json.dumps(response),
            timeout_multiplier = 1,
            timeout = 1, 
            max_retries = 1,
            exception_name = TrackTransaction.ExceptionType.PENDING.label,
        )
    
    def test_pending_transaction_task(self):
        response= tsk_track_transaction(self.exception_transaction.id)
        self.assertIn("status", response.keys())
        self.assertIn("message", response.keys())
    
    def test_server_down_task(self):
        pass
    
    def test_server_error_task(self):
        response = Munch({
            'ReplyCode': '210', 
            'ReplyMessage': 'Unable to process: General Error  on the Prepaid platform. Please try again later. HOT Recharge'})
        
        self.exception_transaction.response = json.dumps(response)
        self.exception_transaction.exception_name = TrackTransaction.ExceptionType.SERVICE_ERROR.label
        self.exception_transaction.save()
        
        response = tsk_track_transaction(self.exception_transaction.id)
        self.assertIn("status", response.keys())
        self.assertIn("message", response.keys())

class AirtimeFulfillmentTestCase(TestCase):
    
    def setUp(self):
        response = Munch({
            'Status': 'pending',
            'ReplyCode': 4, 
            'ReplyMsg': 'Pending ZESA Token Purchase of $675.00 for 01620187847. \r\nPlease check transaction in 5 minutes to see if status has been updated by Service Provider.\r\nThank you for choosing HOT Recharge', 
            'WalletBalance': 0.0, 
            'Amount': 675.0, 
            'ProviderFees': 0.0, 
            'Discount': 0.0, 
            'Meter': '01620187847', 
            'AccountName': '', 
            'Address': '', 
            'Tokens': [], 
            'AgentReference': '', 
            'RechargeID': 111591104, 
            'CustomerInfo': 
                Munch({
                    'Reference': '', 
                    'CustomerName': '', 
                    'Address': '', 
                    'MeterNumber': '01620187847'
                    })
        })
        
        user = User.objects.create_user(
            fake.name(), 
            "johnwick@mail.com", 
            fake.password(), 
            first_name=fake.first_name(), 
            last_name=fake.last_name())
        
        new_trans  = Transaction.objects.create(
            gateway = "unknown",
            transaction_id = user.username +"-" + get_timestamp(),
            status = Transaction.Status.WAITING_PAYMENT.label,
            total_amount = 3.00,
        )
        
        new_trans.save()
        self.order = Order.objects.create(
            user=user, 
            transaction= new_trans,
            operator="Econet", 
            mobile_number="0778548832",
            service=Order.Service.AIRTIME.label,
            meter_number= "01620187847",
            total= 40000.00,
            airtime_amount=40000.00
        )
        
        self.exception_transaction = TrackTransaction.objects.create(
            order = self.order,
            user = user,
            request =json.dumps(Munch({
                "host": "127.0.0.1:8000",
                "scheme": "http",
                "email": "madechangu.takunda@gmail.com",
                "user_id": 36
            })),
            response = json.dumps(response),
            timeout = 1, 
            timeout_multiplier = 1,
            max_retries = 1,
            exception_name = TrackTransaction.ExceptionType.SERVICE_ERROR.label,
        )
    
    def test_insufficient_balanace_task(self):
        response = Munch({'ReplyCode': '208', 'ReplyMessage': 'Your recharge for mobile 0772358338 failed due to insufficient balance.\r\nYour balance is $5,705.72.\r\nYou can sell approximately $5,799.09. HOT Recharge.'})
        self.exception_transaction.response = json.dumps(response)
        self.exception_transaction.exception_name = TrackTransaction.ExceptionType.INSUFFICIENT_BALANCE.label
        self.exception_transaction.save()
        
        self.order.total = 280000.00
        self.order.airtime_amount = 28000.00
        self.order.save()
        
        response = tsk_track_transaction(self.exception_transaction.id)
        self.assertIn("status", response.keys())
        self.assertIn("message", response.keys())
    
    def test_limit_error_task(self):
        response = Munch({'ReplyCode': '222', 'ReplyMessage': 'Your recharge request was too much or too little. Minimum Recharge 0.1 Maximum Recharge 30,000.00, try in the correct range. HOT Recharge\r\n'})
        self.exception_transaction.response = json.dumps(response)
        self.exception_transaction.exception_name = TrackTransaction.ExceptionType.LIMIT_ERROR.label
        self.exception_transaction.save()
        
        self.order.total = 400000.00
        self.order.airtime_amount = 400000.00
        self.order.save()
        
        response  = tsk_track_transaction(self.exception_transaction.id)
        self.assertIn("status", response.keys())
        self.assertIn("message", response.keys())
    
    def test_transaction_down(self):
        pass