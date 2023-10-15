from django.db import models
from django.conf import settings

TYPES = [
    ("BACK-END", "BACK-END"),
    ("FRONT-END", "FRONT-END"),
    ("IOS", "IOS"),
    ("ANDROID", "ANDROID"),
]

PRIORITIES = [("LOW", "LOW"), ("MEDIUM", "MEDIUM"), ("HIGH", "HIGH")]

TAGS = [("BUG", "BUG"), ("FEATURE", "FEATURE"), ("TASK", "TASK")]

STATUSES = [("TODO", "TODO"), ("IN_PROGRESS", "IN_PROGRESS"), ("FINISHED", "FINISHED")]


class Projects(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=100, choices=TYPES)


class Contributors(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)


class Issues(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=8192)
    priority = models.CharField(
        max_length=20, choices=PRIORITIES, blank=False, default="LOW"
    )
    tag = models.CharField(max_length=20, choices=TAGS, blank=False)
    status = models.CharField(
        max_length=20, choices=STATUSES, default="TODO", blank=False
    )
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    assigned_user_id = models.ForeignKey(Contributors, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=8192)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
