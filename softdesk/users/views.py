from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from projects.models import Projects, Contributors, Issues, Comments
from users.serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from projects.permissions import IsCurrentUser
from django.shortcuts import get_object_or_404


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get_permissions(self):
        if (
            self.action == "update"
            or self.action == "destroy"
            or self.action == "delete_all_data"
        ):
            permission_classes = [IsCurrentUser, IsAuthenticated]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        queryset = User.objects.filter(id=pk)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(instance=user, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete_all_data(self, request, pk=None):
        User.objects.filter(id=pk).delete()
        Projects.objects.filter(author=pk).delete()
        Contributors.objects.filter(user=pk).delete()
        Issues.objects.filter(author_user_id=pk).delete()
        Comments.objects.filter(author_user_id=pk).delete()

        return Response({"message: All your data have been deleted"})


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
