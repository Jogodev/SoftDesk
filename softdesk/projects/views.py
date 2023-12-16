from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from projects.permissions import (
    IsProjectAuthor,
    IsContributor,
    IsIssueAuthor,
    IsCommentAuthor,
)
from projects.models import Projects, Contributors, Issues, Comments
from users.models import User
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


class ProjectViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        if self.action == "update" or self.action == "destroy":
            permission_classes = [IsProjectAuthor]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data_copy = request.data.copy()
        new_contributor = request.user.id
        data_copy["author"] = new_contributor
        serializer = ProjectSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Projects.objects.get(id=serializer.data["id"])
        Projects.objects.create(author=request.user)
        Contributors.objects.create(user=request.user, project=project_instance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data_copy = request.data.copy()
        new_contributor = request.user.id
        data_copy["author"] = new_contributor
        queryset = Projects.objects.filter(id=pk)
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(instance=project, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Projects.objects.get(id=serializer.data["id"])
        Contributors.objects.create(user=request.user, project=project_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def project_subscription(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        if Contributors.objects.filter(user=request.user, project=project):
            return Response(
                {"message": "You already contribute to this project"},
                status=status.HTTP_418_IM_A_TEAPOT,
            )
        else:
            Contributors.objects.create(user=request.user, project=project)
        return Response(status=status.HTTP_200_OK)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributors.objects.all()

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        if self.action == "update" or self.action == "destroy":
            permission_classes = [IsProjectAuthor, IsAuthenticated]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAuthenticated, IsContributor]
            return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None):
        serializer = self.serializer_class(
            self.queryset.filter(project=self.kwargs["project_pk"]), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, project_pk=None):
        data_copy = request.data.copy()
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project = Projects.objects.get(id=data_copy["project"])
        user = User.objects.get(id=data_copy["user"])
        Contributors.objects.create(user=user, project=project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, project_pk=None):
        contributor = get_object_or_404(self.queryset, pk=pk, project=project_pk)
        self.perform_destroy(contributor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issues.objects.all()

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        if self.action == "update" or self.action == "destroy":
            permission_classes = [IsIssueAuthor, IsAuthenticated]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAuthenticated,  IsContributor]
            return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, project_pk=None):
        data_copy = request.data.copy()
        data_copy["project"] = project_pk
        data_copy["author_user_id"] = request.user.id
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, project_pk=None):
        data_copy = request.data.copy()
        data_copy["project"] = project_pk
        data_copy["author_user_id"] = request.user.id
        queryset = Issues.objects.filter(id=pk)
        issue = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(instance=issue, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, project_pk=None):
        issue = get_object_or_404(self.queryset, pk=pk, project=project_pk)
        self.perform_destroy(issue)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        if self.action == "update" or self.action == "destroy":
            permission_classes = [IsCommentAuthor, IsAuthenticated]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAuthenticated, IsContributor]
            return [permission() for permission in permission_classes]

    def list(self, request, project_pk=None, issue_pk=None):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, project_pk=None, issue_pk=None):
        data_copy = request.data.copy()
        issue = Issues.objects.get(pk=issue_pk)
        data_copy["author_user_id"] = request.user.id
        data_copy["issue_id"] = issue.id
        serializer = self.serializer_class(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        data_copy = request.data.copy()
        issue = Issues.objects.get(pk=issue_pk)
        data_copy["author_user_id"] = request.user.id
        data_copy["issue_id"] = issue.id
        queryset = Comments.objects.filter(id=pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(instance=comment, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
