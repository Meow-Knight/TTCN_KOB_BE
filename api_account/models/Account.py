from django.db import models
from django.contrib.auth.models import AbstractUser

from api_account.models import Role
from django.contrib.auth.models import UserManager


class Account(AbstractUser):
    objects = UserManager()
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "account"
        ordering = ('date_joined',)
