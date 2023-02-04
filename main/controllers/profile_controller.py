from django.shortcuts import redirect, render
from django.http import JsonResponse
from app_auth.models import User
from main.models import Order
from django.contrib.auth.decorators import login_required
from app_utils.helpers import put_error_message, put_success_message
from django.urls import reverse
from django.contrib.auth import authenticate

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'welcome back', {'orders': orders, 'pagename': 'orders'})

@login_required
def user_password(request):
    if request.method == "POST":
        existing_password = request.POST.get('existing_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = authenticate(request, username=request.user.username, password=existing_password)

        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                put_success_message(request, 'Your password has been changed.')
            else:
                put_error_message(request, 'Passwords do not match.')
        else:
            put_error_message(request, 'Incorrect old password.')
        
        
    return render(request, '/', {
        'pagename': 'change_password',
    })


@login_required
def user_profile(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        put_success_message(request, "Details saved") 
        return redirect(reverse("user-profile"))
        
        
    
    
    
    return render(request, '/', {
        'pagename': 'personal',
    })
    