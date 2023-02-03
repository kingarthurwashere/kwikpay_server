from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    class Types(models.TextChoices):
        MANAGER = "MANAGER"
        REGULAR = "REGULAR"
        
    user_type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.REGULAR.label)

    def __str__(self):
        return self.username



    