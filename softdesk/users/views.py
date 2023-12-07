from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class RegisterViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request):
        can_data_be_shared = False
        can_be_contacted = False
        if request.POST.get("can_data_be_shared", True):
            can_data_be_shared = True
        if request.POST.get("can_be_contacted", True):
            can_be_contacted = True
    
        user = User(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
            date_of_birth=request.data["date_of_birth"],
            can_data_be_shared=can_data_be_shared,
            can_be_contacted=can_be_contacted,
        )
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
