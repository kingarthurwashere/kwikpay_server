import json
from main.models import Order
from fulfillment.controllers.airtime_fulfillment_controller import buy_airtime_for_user
from fulfillment.controllers.zesa_fulfillment_controller import buy_zesa_for_user
from transactions.models import AirtimeTransaction, Transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from app_utils.helpers import get_current_date, get_custom_request, json_error_response, ResponseStatus,  json_success_response, put_error_message
from django.views.decorators.csrf import csrf_exempt

def check_payment_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        
        if order.transaction.paid == True:
            if order.fulfilled == False:
                if order.service == Order.Service.AIRTIME.label:
                    return buy_airtime_for_user(request, order)
                elif order.service == Order.Service.ELECTRIC_BILL.label:
                    return buy_zesa_for_user(request, order)
            else:
                message = "Your order has already been fulfilled"
                resp_data = {
                        "OrderID": order.id, 
                        'FullfilledStatus': order.fulfilled
                }
                
                
                return json_success_response(ResponseStatus.SUCCESS, message, resp_data)
        else:
            message = "Order not paid yet"
            return json_error_response(request, message, None)
    else: 
        message = "Request should be POST"
        return json_error_response(request, message, None)

@csrf_exempt
def recharge_failed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.transaction.status = Transaction.Status.CANCELLED.label
    order.transaction.gateway = "PayPal"
    order.transaction.save()
    
    
    return render(request, 'failed', {
        'order': order,
        'date': get_current_date()
    })

@csrf_exempt
def recharge_successful(request, order_id):

    order = Order.objects.get(id=order_id)
    order.transaction.status = Transaction.Status.PAYMENT_SUCCESS.label
    order.transaction.save()
    
    return render(request, 'done', {
        'order': order, 
        'date': get_current_date(),
        'username': request.user.username,
    })