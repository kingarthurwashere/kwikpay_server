from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from app_auth.models import User
from main.models import Setting
from main.models import Order, Subscribe
import stripe
from kwikpay_server import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


try:
   stripe_secret_key = Setting.objects.get(name="STRIPE_SECRET_KEY")
   stripe_secret_key = stripe_secret_key.value 
except Setting.DoesNotExist:
    stripe_secret_key = settings.STRIPE_SECRET_KEY

try:
   stripe_webhook_secret = Setting.objects.get(name="STRIPE_WEBHOOK_SECRET")
   stripe_webhook_secret = stripe_webhook_secret.value 
except Setting.DoesNotExist:
   stripe_webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
stripe.api_key = stripe_secret_key



@csrf_exempt
def stripe_webhooks(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return JsonResponse({ 'status': 'failed', 'message': e.__str__()})
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return JsonResponse({ 'status': 'failed', 'message': e.__str__()})

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        
        
        try:
            session = event['data']['object']
            customer_email = session["customer_email"]
            order_id = session["metadata"]["order_id"]
        except KeyError as e:
            print(e)
            return JsonResponse({ 'status': 'failed', 'message': 'Key Error: ' + e.__str__()})
    

        order = Order.objects.get(id=order_id)
        order.transaction.paid = True
        order.transaction.payment_date = get_current_date()
        order.transaction.customer_email  = customer_email
        order.transaction.gateway = "Stripe"
        order.transaction.save()
        print("order updated")
        
        #TODO: Send email to user
        send_mail(
            subject="Payment Update",
            message=f"Your payment was successful",
            recipient_list=[customer_email],
            from_email="your@email.com"
        )

        return JsonResponse({
            "status": "success",
            "message": "Sucessfully paid"
        })
    
    
def get_stripe_session(request):
    
    if request.method == "POST":
        order_id = request.POST.get("order_id")
    
        order = Order.objects.get(id=order_id)
        protocol = request.scheme
        
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
            line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(order.total * 100),
                            'product_data': {
                                'name': order.service
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "order_id": order.id
                },
                mode='payment',
                success_url='{}://{}/{}/{}'.format(protocol, request.get_host(),
                                           'payment-done', order_id),
                cancel_url= '{}://{}/{}/{}'.format(protocol, request.get_host(),
                                              'payment-cancelled', order_id),
            )
        return JsonResponse({
            'status': "success",
            'session_id': checkout_session.id
        })
