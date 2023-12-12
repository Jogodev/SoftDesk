from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, date
from projects.models import Projects


class User(AbstractUser):
    date_of_birth = models.DateField("date_of_birth", blank=False, default=date.today)
    password2 = models.CharField(max_length=128, verbose_name="password2", blank=True)
    project = models.ManyToManyField(Projects)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    username = models.CharField(
        verbose_name="username",
        unique=True,
        max_length=50,
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "date_of_birth",
    ]

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
