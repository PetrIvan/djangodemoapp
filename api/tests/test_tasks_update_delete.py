import tempfile

from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Task
from .task_factory import prepare_dummy_image, validate_processed_image


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TaskAPITest(APITestCase):
    def setUp(self):
        self.payload = {
            "title": "A test task with a photo",
            "description": "A test description",
            "due_date": "2030-12-31",
            "photo": prepare_dummy_image(),
        }

        task_list_url = reverse("tasks")
        response = self.client.post(task_list_url, self.payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.task_id = response.data["id"]
        self.url = reverse("task-update-delete", args=[self.task_id])

        self.invalid_url = reverse("task-update-delete", args=[999999])

    def test_get_task_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.payload["title"])
        self.assertEqual(response.data["description"], self.payload["description"])
        self.assertIn("photo", response.data)

    def test_get_nonexistent_task(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task(self):
        new_payload = {
            "title": "A test task with a different title and photo",
            "photo": prepare_dummy_image(),
        }

        # Verify that task update works
        response = self.client.put(self.url, new_payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], new_payload["title"])
        self.assertIn("photo", response.data)

        # Validate the processed image
        task = Task.objects.get(id=self.task_id)
        self.assertIsNotNone(task)
        self.assertIsNotNone(task.photo)

        is_valid_dimension, is_grayscale = validate_processed_image(task.photo.path)
        self.assertTrue(is_valid_dimension, "Image exceeds maximum dimension allowed")
        self.assertTrue(is_grayscale, "Image is not grayscale")

    def test_delete_task(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the task was deleted
        self.assertEqual(Task.objects.filter(id=self.task_id).count(), 0)

    def test_delete_nonexistent_task(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
