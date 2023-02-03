
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives

from main.models import Order
from transactions.models import Transaction
import json


def show_success_template(request):
    return render(request, 'appemail/success/zesa.html', {})




def send_airtime_success(order_id, customer_email, scheme, host):
    order = Order.objects.get(id=order_id)
    
    subject = 'Transaction Success'
    html_template = 'appemail/success/airtime.html'
    html_template_data = {'order': order, 'scheme': scheme, 'host': host}
    from_email = 'KwikPay Billing <billing@kwikpay.co.zw>'
    to = customer_email
    
    app_send_email(
        subject,
        html_template,
        html_template_data,
        from_email,
        to
    )
    
def send_zesa_success(order_id, customer_email, scheme, host):
    order = Order.objects.get(id=order_id)
    transaction_object = json.loads(order.transaction.transaction_object)   
    token = transaction_object['Tokens'][0]
    subject = 'Transaction Success'

    subject = 'Transaction Success'
    html_template = 'appemail/success/zesa.html'
    html_template_data = {'order': order, 'scheme': scheme, 'host': host, 'token': token}
    from_email = 'KwikPay Billing <billing@kwikpay.co.zw>'
    to = customer_email
    
    
    app_send_email(
        subject,
        html_template,
        html_template_data,
        from_email,
        to
    )
    
    