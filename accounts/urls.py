from django.urls import path
from .views import SignUpView, UserView, UserUpdateView

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<str:pk>/", UserView.as_view(), name="user"),
    path(
        "user/<str:pk>/update/", UserUpdateView.as_view(), name="user_update"
    ),
]
