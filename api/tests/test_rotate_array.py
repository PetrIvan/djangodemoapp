from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RotateArrayAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("rotate-array")

    def test_rotate_array(self):
        payload = {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"result": [5, 6, 7, 1, 2, 3, 4]})
