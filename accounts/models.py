from queue import Empty
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    id_number = models.CharField(
        null=False, blank=False, max_length=20, unique=True)
    contact = models.CharField(
        null=False, blank=False, max_length=20, unique=True)
    address = models.TextField(null=False, blank=False, max_length=200)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return (
            str(self.id)
            if self.first_name == "" and self.last_name == ""
            else f"{self.first_name} {self.last_name}"
        )


class Profile(models.Model):
    """User Profile that contains all the contact info"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=250, default="")
    last_name = models.CharField(max_length=250, default="")
    id_number = models.CharField(
        null=True, blank=True, max_length=20, default="")
    contact = models.CharField(
        null=True, blank=True, max_length=20, default="")
    address = models.TextField(
        null=True, blank=True, max_length=200, default="")

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return (
            self.user.username
            if len(self.first_name) < 1 or len(self.last_name) < 1
            else f"{self.first_name} {self.last_name}"
        )

    def get_absolute_url(self):
        """Getting absolute_url"""
        return reverse("accounts.Profile", kwargs={"pk": self.id})
