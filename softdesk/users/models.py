from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    date_of_birth = models.DateField(blank=False, default=datetime.now)
    password2 = models.CharField(max_length=128, verbose_name="password2", blank=True)
