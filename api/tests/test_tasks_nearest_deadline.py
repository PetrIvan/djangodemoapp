from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TaskAPITest(APITestCase):
    def setUp(self):
        self.task_list_url = reverse("tasks")

        self.now = timezone.now()
        self.tomorrow = (self.now + timedelta(days=1)).date()

        self.add_task_with_offset("A task in the past", days=-1)
        self.add_task_with_offset("A task in the near future", days=1)
        self.add_task_with_offset("A task in the far future", days=3)

        self.payload = {
            "title": "A task without a deadline",
        }
        response = self.client.post(self.task_list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.url = reverse("task-nearest-deadline")

    def add_task_with_offset(self, title: str, days: int):
        self.payload = {
            "title": title,
            "due_date": (self.now + timedelta(days=days)).date().isoformat(),
        }

        response = self.client.post(self.task_list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_nearest_deadline(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["due_date"])

        # The nearest task is tomorrow
        self.assertEqual(response.data["due_date"], self.tomorrow.isoformat())
