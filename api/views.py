import heapq

from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, RotateArraySerializer, KthLargestSerializer
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

    serializer_class = TaskSerializer

    def get(self, request: Request, id: int) -> Response:
        """Retrieve a specific task"""
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, id: int) -> Response:
        """Update a specific task"""
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                task = serializer.save()
                process_task_image(task)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, id: int) -> Response:
        """Delete a specific task"""
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TaskNearestDeadlineAPIView(APIView):
    serializer_class = TaskSerializer

    def get(self, request: Request) -> Response:
        """Finds a task with the nearest deadline"""

        # Filter out tasks without deadline, sort them
        tasks = Task.objects.filter(due_date__isnull=False).order_by("due_date")

        # Filter out tasks in the past, get the first
        nearest = tasks.filter(due_date__gt=timezone.now()).first()

        serializer = TaskSerializer(nearest)
        return Response(serializer.data)


class RotateArrayAPIView(APIView):
    serializer_class = RotateArraySerializer

    def post(self, request: Request) -> Response:
        serializer = RotateArraySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nums: list[int] = serializer.data["nums"]
        k: int = serializer.data["k"] % len(nums)

        nums = nums[-k:] + nums[:-k]

        return Response({"result": nums}, status=status.HTTP_200_OK)


class KthLargestAPIView(APIView):
    serializer_class = KthLargestSerializer

    def post(self, request: Request) -> Response:
        serializer = KthLargestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nums: list[int] = serializer.data["nums"]
        k: int = serializer.data["k"]
        top_k: list[int] = []

        for num in nums:
            # Add the number to the heap
            heapq.heappush(top_k, num)

            # Pop the smallest one, leaving just the top k
            if len(top_k) > k:
                heapq.heappop(top_k)

        # Since we have just the top k elements, the smallest one is kth largest
        kth_largest = heapq.heappop(top_k)
        return Response({"result": kth_largest}, status=status.HTTP_200_OK)
