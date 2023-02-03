from django.contrib import admin
from app_auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'user_type', 'first_name', 'last_name', 'email', 'is_active', 'date_joined']

# Register your models here.
admin.site.register(User, UserAdmin)
