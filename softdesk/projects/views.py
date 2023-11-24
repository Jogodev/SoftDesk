from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        author = request.user
        new_contributor = User.objects.filter(id=data_copy["author"])[0]
        data_copy["author"] = new_contributor.id
        serializer = ProjectSerializer(data=data_copy)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Projects.objects.get(id=serializer.data["id"])
        Projects.objects.create(author=request.user,)
        Contributors.objects.create(user=new_contributor, project=project_instance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        queryset = Projects.objects.filter(id=pk)
        new_contributor = User.objects.filter(id=data_copy["author"])[0]
        data_copy["author"] = new_contributor.id
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(instance=project, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Projects.objects.get(id=serializer.data["id"])
        Contributors.objects.create(user=new_contributor, project=project_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributors.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project = Projects.objects.get(id=data_copy["project"])
        user = User.objects.get(id=data_copy["user"])
        Contributors.objects.create(user=user, project=project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        contributor = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(contributor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issues.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_id = Projects.objects.get(id=ProjectSerializer.data["id"])
        assigned_user_id = Contributors.objects.filter(id=project_id)
        Issues.objects.create(
            author_user_id=request.user,
            project=project_id,
            assigned_user_id=assigned_user_id,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        queryset = Issues.objects.filter(id=pk)
        issue = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(instance=issue, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        issue = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(issue)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        issue_id = Issues.objects.get(id=IssueSerializer.data["id"])
        Comments.objects.create(
            author_user_id=request.user,
            issue_id=issue_id,
        )

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        queryset = Comments.objects.filter(id=pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(instance=comment, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
