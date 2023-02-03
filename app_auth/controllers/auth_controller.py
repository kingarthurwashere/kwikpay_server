from django.contrib.auth import authenticate, login as auth_login, logout
from app_auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from app_auth.tasks import tsk_send_welcome_message, tsk_send_password_reset

def register(request):
    if request.method == "POST":
        username = request.POST.get("email").split("@")[0]
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        destination_url = request.POST.get("destination_url")
        
        
        try:
            first_name = full_name.split(" ")[0]
            last_name = full_name.split(" ")[1]
        except IndexError:
            first_name = full_name
            last_name = ""
            
      
        # Email checks
        if len(User.objects.filter(email=email)) > 0:
            put_error_message(request, "Email already exists")
        elif len(User.objects.filter(username=username)) > 0:
            put_error_message(request, "Username is taken!")
        else:
            if is_email(email) and is_password_valid(password):
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                user.save()
                put_success_message(request, "Registration successful")
                
                
                tsk_send_welcome_message.delay(
                    first_name,
                    email,
                    request.scheme,
                    request.get_host()
                )
            else:
                put_error_message(request, "Invalid email or password")
                    
                    
        if (destination_url == None):
            destination_url = '/accounts/login/'
                
        return redirect(destination_url)
    else:
        page_seo = get_page_seo("register")

        
                         
def logout_page(request):
    logout(request)
    put_success_message(request, "Logout successful")
    return redirect("/")

def password_reset(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        
        if is_email(email):
            user = User.objects.get(email=email)
            
            request = get_custom_request(request)
            tsk_send_password_reset.delay(request, user.id, email)
            return redirect(reverse("password_reset_done"))
    
    
    return render(request, "app_auth/password_reset.html", {})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        destination_url = request.POST.get("destination_url")
        
        user = authenticate(request, username=email.split("@")[0], password=password)

        if user is not None:
            auth_login(request, user)
            put_success_message(request, "Login successful")

        else:
            put_error_message(request, "Login failed")
            
        

        return redirect(destination_url)
    else:
        next_value = request.GET.get("next")
        
        if (next_value == None or next_value == ""):
            next_value = "/"
            
        page_seo = get_page_seo("login")
            
        return render(request, "app_auth/login.html", {"next": next_value, 'seo': page_seo})
    
    
