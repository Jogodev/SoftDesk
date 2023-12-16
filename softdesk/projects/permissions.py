from rest_framework.permissions import BasePermission
from projects.models import Projects, Contributors, Issues, Comments
from users.models import User


class IsCurrentUser(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(id=view.kwargs["pk"])
        return bool(request.user.id == user.id)


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["pk"])
        return bool(request.user == project.author)


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["project_pk"])
        contributors = Contributors.objects.filter(project=project)
        contributor_ids = [contributor.user.id for contributor in contributors]
        return bool(request.user.id in contributor_ids)


class IsIssueAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["project_pk"])
        issue = Issues.objects.get(project=project, id=view.kwargs["pk"])
        return bool(request.user.id == issue.author_user_id.id)


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs["project_pk"])
        issue = Issues.objects.get(project=project, id=view.kwargs["issue_pk"])
        comment = Comments.objects.get(issue_id=issue, id=view.kwargs["pk"])
        return bool(request.user == comment.author_user_id)
