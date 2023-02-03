from app_utils.helpers import app_send_email
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from app_auth.models import User

def send_welcome_user_mail(username, user_email, scheme, host):
  
    subject = 'Welcome ' + username

    html_template = 'appemail/success/welcome.html'
    html_template_data = {'scheme': scheme, 'host': host, 'username': username}
    from_email = 'KwikPay <hello@kwikpay.co.zw>'
    to = user_email
    
    
    app_send_email(
        subject,
        html_template,
        html_template_data,
        from_email,
        to
    )
    
    
def send_password_reset_mail(request, user_id, email):
    
    user = User.objects.get(id=user_id)
    
    subject = 'Password Reset'
    html_template = 'app_auth/password_reset_email.html'
    html_template_data = {
                "user": user,
                "uid":  urlsafe_base64_encode(force_bytes(user.id)),
                "token": default_token_generator.make_token(user),
                "scheme": request['scheme'],
                "host": request['host']
            }
    from_email = 'KwikPay Billing <billing@kwikpay.co.zw>'
    to = email
            
    app_send_email(
                subject,
                html_template,
                html_template_data,
                from_email,
                to
            )