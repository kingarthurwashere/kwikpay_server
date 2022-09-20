from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    """Custom User"""

    class Meta(UserCreationForm.Meta):
        """Meta"""

        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "id_number", "contact", "address", "email",
        )

    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    # for fieldname in ["username", "password1", "password2"]:
    #     self.fields[fieldname].help_text = None


class CustomUserChangeForm(UserChangeForm):
    """Change Form"""

    class Meta(UserChangeForm.Meta):
        """Meta"""

        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserUpdateForm(forms.ModelForm):
    """Update"""

    class Meta:
        """Meta"""

        model = CustomUser
        fields = (
            "first_name", "last_name", "id_number", "contact", "address",
        )
