from rest_framework.serializers import ModelSerializer
from projects.models import Projects, Contributors, Issues, Comments


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = "__all__"


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
