from main.models import Order
from transactions.models import Transaction
from django.http import JsonResponse
from django.shortcuts import render
from app_utils.helpers import get_setting, get_timestamp, verify_recaptcha

def create_airtime_order(request):
    if request.method == "POST":
        operator = request.POST.get("operator")
        mobile_number = request.POST.get("mobile_number")
        package_price = request.POST.get("package_price")
        packages = request.POST.get("packages")
        recaptcha = request.POST.get('recaptcha')
        
        response = verify_recaptcha(recaptcha)
        
        if response['success']:
            # Create Transaction 
            new_trans  = Transaction.objects.create(
                gateway = "unknown",
                transaction_id = request.user.username +"-" + get_timestamp(),
                status = Transaction.Status.WAITING_PAYMENT.label,
                total_amount = package_price
            )
            
            new_trans.save()
            

            # Create order
            new_order = Order.objects.create(
                user=request.user, 
                transaction= new_trans,
                operator=operator, 
                mobile_number=mobile_number,
                service=Order.Service.AIRTIME.label,
                total= package_price,
                airtime_amount=package_price
            )
            
            new_order.save()
            
            return JsonResponse({
                "status": "success", 
                "message": "Order created successfully",
                "order_id": new_order.id})
        else:
            return JsonResponse({
                "status": "failed", 
                "message": "Could not verify reCAPTCHA"})

def create_zesa_order(request):
    if request.method == "POST":
        meter_number = request.POST.get("meter_number")
        package_price = request.POST.get("package_price")
        mobile_number = request.POST.get("mobile_number")
        recaptcha = request.POST.get('recaptcha')
        
        response = verify_recaptcha(recaptcha)
        
        if response['success']:
            # Create Transaction 
            new_trans  = Transaction.objects.create(
                gateway = "unknown",
                transaction_id = request.user.username +"-" + get_timestamp(),
                status = Transaction.Status.WAITING_PAYMENT.label,
                total_amount = package_price
            )
            
            new_trans.save()
            

            # Create order
            new_order = Order.objects.create(
                user=request.user, 
                meter_number=meter_number,
                mobile_number=mobile_number,
                transaction= new_trans,
                service=Order.Service.ELECTRIC_BILL.label,
                total= package_price,
                airtime_amount=package_price
            )
            
            new_order.save()
            
            return JsonResponse({
                "status": "success", 
                "message": "Order created successfully",
                "order_id": new_order.id})
        else:
            return JsonResponse({
                "status": "failed", 
                "message": "Could not verify reCAPTCHA"})
        
def recharge_order_summary(request, order_id):
    order = Order.objects.get(id=order_id)
    
    zw_equivalent  = float(order.airtime_amount) * float(get_setting("USD_TO_ZWL_RATE", 120))
    return render(request, '/', {
        'order': order,
        'zw_equivalent': zw_equivalent
    })
           