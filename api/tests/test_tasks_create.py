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
        self.url = reverse("tasks")

    def test_get_empty_task_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_task_without_photo(self):
        payload = {
            "title": "A test task",
            "description": "A test description",
            "due_date": "2030-12-31",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_create_task_with_photo(self):
        payload = {
            "title": "A test task with a photo",
            "photo": prepare_dummy_image(),
        }

        # Verify that task creation works
        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("photo", response.data)

        # Validate the processed image
        task = Task.objects.first()
        self.assertIsNotNone(task)
        self.assertIsNotNone(task.photo)

        is_valid_dimension, is_grayscale = validate_processed_image(task.photo.path)
        self.assertTrue(is_valid_dimension, "Image exceeds maximum dimension allowed")
        self.assertTrue(is_grayscale, "Image is not grayscale")
