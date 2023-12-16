from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import User
from datetime import date
from django.core.exceptions import ValidationError
from datetime import datetime, date


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "date_of_birth",
            "username",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
        ]


class RegisterSerializer(ModelSerializer):
    date_of_birth = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = User
        fields = [
            "email",
            "date_of_birth",
            "username",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_date_of_birth(self, date_of_birth):
        today = date.today()
        date_of_birth = datetime.strptime(str(date_of_birth), "%Y-%m-%d")
        age = (
            today.year
            - date_of_birth.year
            - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        )
        if age < 15:
            raise serializers.ValidationError(
                f"You must be at least 15 years old to register you only have {age} years"
            )
        return datetime.date(date_of_birth)
