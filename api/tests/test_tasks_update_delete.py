import tempfile
import numpy as np
import cv2 as cv

from django.urls import reverse
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TaskAPITest(APITestCase):
    def setUp(self):
        # Prepare a database sample to test
        img = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)
        _, img_encoded = cv.imencode(".jpg", img)
        image_bytes = img_encoded.tobytes()

        image_file = SimpleUploadedFile(
            "test.jpg", image_bytes, content_type="image/jpeg"
        )

        self.payload = {
            "title": "A test task with a photo",
            "description": "A test description",
            "due_date": "2030-12-31",
            "photo": image_file,
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
