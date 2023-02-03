
from main.models import Order, Setting
from django.http import JsonResponse
from kwikpay_server import settings
from django.shortcuts import render, redirect
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.urls import reverse



try:    
    paypal_reciever_email = Setting.objects.get(name='PAYPAL_RECEIVER_EMAIL')
    paypal_reciever_email = paypal_reciever_email.value
except Setting.DoesNotExist:
    paypal_reciever_email = settings.PAYPAL_RECEIVER_EMAIL
    
try:
    stripe_public_key = Setting.objects.get(name='STRIPE_PUBLIC_KEY')
    stripe_public_key = stripe_public_key.value
except Setting.DoesNotExist:
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    





@csrf_exempt
def paypal_notify(request, order_id):
    if request.method == "POST":
        
        mc_gross = request.POST.get("mc_gross")
        invoice = request.POST.get("invoice")
        payment_date = request.POST.get("payment_date")
        payment_status = request.POST.get("payment_status")
        business = request.POST.get("business")
        payer_email = request.POST.get("payer_email")
        reciever_email = request.POST.get("receiver_email")
        order = Order.objects.get(id=order_id)
        
        #...Remove this later
        # payment_status = "Completed"
        
        
        if payment_status == "Completed":
            if reciever_email != paypal_reciever_email:
                print("Invalid receiver email")
                return JsonResponse({"status": "Failed", "message": "Invalid receiver email"})
            
            print("MC Gross: ", mc_gross)
            print("Order Paid: ", order.total)
            
            if str(order.total) == str(mc_gross):
                order.transaction.paid = True
                order.transaction.payment_date = get_current_date()
                order.transaction.customer_email = payer_email
                order.transaction.gateway = "Paypal"
                order.transaction.save()
                
                send_mail(
                    subject="Payment Update",
                    message=f"Your payment was successful",
                    recipient_list=[payer_email],
                    from_email="your@email.com"
                )
                
                return JsonResponse({"status": "success", "message": "Payment successful"})
            else:
                print("Payment not completed: MC_GROSS != Order Amount Paid")
                return JsonResponse({
                    "status": "Failed",
                    "message": "Payment not completed"
                })
        else:
            print("Payment not completed 2")
            return JsonResponse({"status": "Failed", "message": "Payment not completed"})
        
def paypal_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        trans_id  = order.transaction.transaction_id
        protocol = request.scheme
        
       
        
        paypal_dict = {
        'business': paypal_reciever_email,
        'amount': '%.2f' % order.total.quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': trans_id,
        'currency_code': 'USD',
        'notify_url': '{}://{}/{}/{}'.format(protocol, request.get_host(),
                                        'paypal-notify', order_id),
        'return_url': '{}://{}/{}/{}'.format(protocol, request.get_host(),
                                           'payment-done', order_id),
        'cancel_return': '{}://{}/{}/{}'.format(protocol, request.get_host(),
                                              'payment-cancelled', order_id),
    }
        
        # Mark transaction as paypal 
        order.transaction.gateway = "paypal";
        order.transaction.save()
        
        
        return render(request, 'main/payment.html', {
            'order': order, 
            'paypal': paypal_dict, 
            'stripe_public_key': stripe_public_key})
    except Order.DoesNotExist:
        put_error_message(request, 'Order does not exist')
        return redirect("/")