from django.urls import path
from appemail.controllers import transaction_controller
from .controllers import auth_controller
from django.contrib.auth import views as auth_views 

reset_complete_view = auth_views.PasswordResetCompleteView.as_view(template_name='app_auth/password_reset_complete.html')
reset_password_view = auth_views.PasswordResetConfirmView.as_view(template_name="app_auth/password_reset_confirm.html")
request_password_reset_sent_view = auth_views.PasswordResetDoneView.as_view(template_name='app_auth/password_reset_done.html')


urlpatterns =[   
 
 # Auth
 path("login/", auth_controller.login, name="user-login"),
 path("register", auth_controller.register, name="user-register"),
 path("logout", auth_controller.logout_page, name="user-logout"),
 path("password_reset/", auth_controller.password_reset, name="password_reset"),
 path('password_reset/done/', request_password_reset_sent_view, name='password_reset_done'),
 path('reset/<uidb64>/<token>/', reset_password_view, name='password_reset_confirm'),
 path('reset/done/', reset_complete_view, name='password_reset_complete'),      
 
]