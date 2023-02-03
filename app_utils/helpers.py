import re
import datetime

from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPRecipientsRefused
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http.response import JsonResponse
from main.models import Setting
from munch import Munch
from kwikpay_server import settings
import requests 

def get_current_date():
    """
    Returns current date.

    :return:
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_timestamp():
    """
    Returns current timestamp.

    :return:
    """
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def get_timestamp_2():
    import time
    return time.time()

def write_to_file(file_name, content):
    """
    Writes content to file.

    :param file_name:
    :param content:
    :return:
    """
    with open(file_name, 'w') as file:
        file.write(content)

def get_random_string(length=32):
    """
    Get random string
    :return:
    """
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
  

def app_send_email(subject, html_template,html_template_data, from_email, to):
    
    try:
        html_message = render_to_string(html_template,html_template_data )
        plain_message = strip_tags(html_message)
        
        msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        msg.attach_alternative(html_message, "text/html")
        msg.send()
    except SMTPRecipientsRefused as e:
        print("[App Send Mail] -> Recipient refused")
    


def is_email(email):
    """
    Checks if email is valid.

    :param email:
    :return:
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

def is_password_valid(password):
    """
    Checks if password is valid.

    :param password:
    :return:
    """
    if len(password) < 8:
        return False
    return True

def put_success_message(request, message):
    """
    Puts success message into session.

    :param request:
    :param message:
    :return:
    """
    
    if "success_messages" not in request.session.keys():
        request.session['success_messages'] = [] 
        
    request.session['success_messages'].append({
        "message": message
    })
    
def put_error_message(request, message):
    """
        Puts error message into session.

        :param request:
        :param message:
        :return:
    """
    
    if "error_messages" not in request.session.keys():
        request.session['error_messages'] = []       
    
    request.session['error_messages'].append({
            "message": message
        })
    
    
class ResponseStatus:
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    
    

def json_success_response(status, message, data=None):  
  response_object = {
                "status": status, 
                "message": message,
                "data": data              
    }
    
  return JsonResponse(response_object)


def json_error_response(request, message, data=None):  
  response_object = {
                "status": "error", 
                "message": message,
                "data": data              
    }
    
  return JsonResponse(response_object)


def get_setting(name, default):
    try:
        result = Setting.objects.get(name=name).value
    except Setting.DoesNotExist:
        result = default
        
    return result

def get_custom_request(request):
    custom_req = Munch()
    
    custom_req.host = request.get_host()
    custom_req.scheme = request.scheme
    custom_req.path = request.path
    
    try:
        custom_req.email = request.user.email
        custom_req.user_id = request.user.id
    except AttributeError:
        custom_req.email = None
        custom_req.user_id = None


        
    
    return custom_req

def get_page_seo(page_name):
    try:
        seo = SEO.objects.get(page_name=page_name)
    except:
        seo = SEO.objects.get(page_name="default")
        
    return seo


def verify_recaptcha(recaptcha_resp):
    req_data = {
		    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_resp
		}
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=req_data)
    return r.json()

    