from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer
from .image_processing import process_task_image


class TaskListCreateAPIView(APIView):
    """Handles listing and creating tasks"""

    serializer_class = TaskSerializer

    def get(self, request: Request) -> Response:
        """Retrieve all tasks"""
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Create a new task"""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task: Task = serializer.save()
            process_task_image(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateDeleteAPIView(APIView):
    """Handles operations on a specific task"""

    def get(self, request: Request, id: int) -> Response:
        """Retrieve a specific task"""
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
