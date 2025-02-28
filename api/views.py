import cv2 as cv

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


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

            if task.photo:
                img = cv.imread(task.photo.path)
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # Limit to 800x800 px without distortion
                max_size = max(img.shape[0], img.shape[1])
                if max_size > 800:
                    compression_factor = max_size / 800
                    img = cv.resize(
                        img,
                        (
                            int(img.shape[1] / compression_factor),
                            int(img.shape[0] / compression_factor),
                        ),
                    )

                cv.imwrite(task.photo.path, img)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
