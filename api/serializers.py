from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "photo"]


class RotateArraySerializer(serializers.Serializer):
    nums = serializers.ListField(child=serializers.IntegerField())
    k = serializers.IntegerField()


class KthLargestSerializer(serializers.Serializer):
    nums = serializers.ListField(child=serializers.IntegerField())
    k = serializers.IntegerField()


class LongestIncreasingPathSerializer(serializers.Serializer):
    matrix = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(), allow_empty=False
        ),
        allow_empty=False,
    )

    def validate_matrix(self, value):
        if not all(len(row) == len(value[0]) for row in value):
            raise serializers.ValidationError("All rows must have the same length.")
        return value
