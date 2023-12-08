from rest_framework.permissions import BasePermission
from projects.models import Projects, Contributors, Issues, Comments


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["pk"])
        return bool(request.user == project.author)


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs['project_pk'])
        contributor = Contributors.objects.get(project=project, id=view.kwargs['pk'])
        return bool(request.user == contributor.user)


class IsIssueAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["project_pk"])
        issue = Issues.objects.get(project=project, id=view.kwargs["pk"])
        return bool(request.user == issue.author_user_id)


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["project_pk"])
        issue = Issues.objects.get(project=project, id=view.kwargs["issue_pk"])
        comment = Comments.objects.get(issue_id=issue, id=view.kwargs["pk"])
        return bool(request.user == comment.author_user_id)
