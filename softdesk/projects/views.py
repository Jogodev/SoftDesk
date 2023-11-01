from django.shortcuts import get_object_or_404
from projects.models import Projects, Contributors, Issues, Comments
from projects.serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        new_contributor = User.objects.filter(id=data_copy["author"])[0]
        data_copy["author"] = new_contributor.id
        serializer = ProjectSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Projects.objects.get(id=serializer.data["id"])
        Contributors.objects.create(user=new_contributor, project=project_instance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        queryset = Projects.objects.filter(id=pk)
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(instance=project, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributors.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        project_instance = Projects.objects.get(id=ProjectSerializer.data["id"])
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        Contributors.objects.create(user=request.user, project=project_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        contributor = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(contributor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issues.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
