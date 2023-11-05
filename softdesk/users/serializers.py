from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import User
from datetime import date


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

    def age_validate(self, attrs):
        print("age_validate")
        date_of_birth = attrs["date_of_birth"]
        today = date.today()
        age = (
            today.year
            - date_of_birth.year
            - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        )
        print("age", age)
        print("dob", date_of_birth)
        # if age < 15:
        #     raise serializers.ValidationError(
        #         "Vous devez avoir au moins 15 ans pour vous inscrire"
        #     )
