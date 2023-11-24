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

    # @property
    # def validate_age(self):
    #     print("age_validate")

    #     if self.compute_age < 15:
    #         raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire")
    #     else:
    #         return True

    # @property
    # def compute_age(self):
    #     print("compute_age")
    #     date_of_birth = datetime.strptime(self.date_of_birth, '%Y-%m-%d')
    #     today = date.today()
    #     age = (
    #         today.year
    #         - date_of_birth.year
    #         - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    #     )
    #     print("age", age)
    #     print("dob", date_of_birth)
    #     return age
