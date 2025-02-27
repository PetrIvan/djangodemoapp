from django.db import models


class Task(models.Model):
    title: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField(
        max_length=500, blank=True, null=True
    )
    due_date: models.DateField = models.DateField(blank=True, null=True)
    photo: models.ImageField = models.ImageField(
        upload_to="tasks/", blank=True, null=True
    )
