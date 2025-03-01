import tempfile
import numpy as np
import cv2 as cv

from django.urls import reverse
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Task


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
        # Prepare a dummy image and payload
        img = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)
        _, img_encoded = cv.imencode(".jpg", img)
        image_bytes = img_encoded.tobytes()

        image_file = SimpleUploadedFile(
            "test.jpg", image_bytes, content_type="image/jpeg"
        )

        payload = {
            "title": "A test task with a photo",
            "photo": image_file,
        }

        # Verify that task creation works
        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("photo", response.data)

        # Validate the processed image
        task = Task.objects.first()
        self.assertIsNotNone(task)
        self.assertIsNotNone(task.photo)

        processed_img = cv.imread(task.photo.path, cv.IMREAD_UNCHANGED)

        h, w = processed_img.shape[:2]
        self.assertLessEqual(h, 800, "Height exceeds 800px")
        self.assertLessEqual(w, 800, "Width exceeds 800px")
        self.assertEqual(len(processed_img.shape), 2, "Image is not grayscale")
