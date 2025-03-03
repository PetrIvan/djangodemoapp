from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "photo"]


class RotateArraySerializer(serializers.Serializer):
    nums = serializers.ListField(child=serializers.IntegerField())
    k = serializers.IntegerField()
