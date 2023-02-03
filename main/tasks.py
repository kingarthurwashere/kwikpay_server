from celery import shared_task
from appemail.controllers import transaction_controller
from munch import Munch

@shared_task(name='send_user_airtime_success_email')
def send_airtime_success_email(request, order_id):
    customer_email = request['email']
    scheme = request['scheme']
    host = request['host']
    
    transaction_controller.send_airtime_success(order_id, customer_email, scheme, host)
    

@shared_task(name='send_user_zesa_success_email')
def send_zesa_success_email(request, order_id):
    customer_email = request["email"]
    scheme = request["scheme"]
    host = request["host"]
    transaction_controller.send_zesa_success(order_id, customer_email, scheme, host)