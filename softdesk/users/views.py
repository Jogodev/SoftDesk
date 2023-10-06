from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
