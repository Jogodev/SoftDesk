from django.db import models
from django.conf import settings

TYPES = [
    ("BACK-END", "BACK-END"), ("FRONT-END", "FRONT-END"), ("IOS", "IOS"), (
        "ANDROID", "ANDROID"
    )
]


class Project(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=100, choices=TYPES)


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
