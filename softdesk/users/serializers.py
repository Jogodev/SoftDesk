from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "date_of_birth", "username", "password", "password2"]
