from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
            date_of_birth=request.data["date_of_birth"],
            can_data_be_shared=request.data["can_data_be_shared"],
            can_be_contacted=request.data["can_be_contacted"]
        )
        serializer = self.serializer_class
        serializer.is_valid(raise_exception=True)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
